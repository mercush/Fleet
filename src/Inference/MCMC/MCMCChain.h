#pragma once 

#include <utility>
#include <functional>
#include "Coroutines.h"
#include "MCMCChain.h"
#include "FiniteHistory.h"
#include "Control.h"
#include "OrderedLock.h"
#include "FleetStatistics.h"

//#define DEBUG_MCMC 1

/**
 * @class MCMCChain
 * @author Steven Piantadosi
 * @date 25/10/21
 * @file MCMCChain.h
 * @brief This represents an MCMC hain on a hypothesis of type HYP. It uses HYP::propose and HYP::compute_posterior
 * 		  to implement MetropolicHastings. 
 */
template<typename _HYP> 
class MCMCChain {
	
public:
	using HYP = _HYP;
	
	 HYP current;
	
	// It's a little important that we use an OrderedLock, because otherwise we have
	// no guarantees about chains accessing in a FIFO order. Non-FIFO is especially
	// bad for ParallelTempering, where there are threads doing the adaptation etc. 
	mutable OrderedLock current_mutex; 
	
	typename HYP::data_t* data;
	
	// this stores the maximum found since we've restarted
	// (not the overall max)
	double maxval;
	
	unsigned long samples; // total number of samples we've done
	unsigned long proposals;
	unsigned long acceptances;
	unsigned long steps_since_improvement; 
	
	std::atomic<double> temperature; // make atomic b/c ParallelTempering may try to change 
	
	FiniteHistory<bool> history;
	
	MCMCChain(HYP& h0, typename HYP::data_t* d) : 
			current(h0), data(d), maxval(-infinity), 
			samples(0), proposals(0), acceptances(0), steps_since_improvement(0),
			temperature(1.0), history(100) {
			runOnCurrent();
	}
	
	MCMCChain(HYP&& h0, typename HYP::data_t* d) : 
			current(h0), data(d), maxval(-infinity),
			samples(0), proposals(0), acceptances(0), steps_since_improvement(0),
			temperature(1.0), history(100) {
			runOnCurrent();
	}

	MCMCChain(const MCMCChain& m) :
		current(m.current), data(m.data), maxval(m.maxval),
		samples(m.samples), proposals(m.proposals), acceptances(m.acceptances), 
		steps_since_improvement(m.steps_since_improvement)	{
		temperature = m.temperature.load();
		history     = m.history;
		
	}
	MCMCChain(MCMCChain&& m) {
		current = m.current;
		data = m.data;
		maxval = m.maxval;
		samples = m.samples;
		proposals = m.proposals;
		acceptances = m.acceptances;
		steps_since_improvement = m.steps_since_improvement;
		
		temperature = m.temperature.load();
		history = std::move(m.history);		
	}
	
	virtual ~MCMCChain() { }
	
	/**
	 * @brief Set this data
	 * @param d - what data to set
	 * @param recompute_posterior - should I recompute the posterior on current?
	 */
	void set_data(typename HYP::data_t* d, bool recompute_posterior=true) {
		data = d;
		if(recompute_posterior) {
			current.compute_posterior(*data);
		}
	}
	
	HYP& getCurrent() {
		/**
		 * @brief get a reference to the current value
		 * @return 
		 */		
		return current; 
	}
	
	const HYP& getCurrent() const {
		/**
		 * @brief get a reference to the current value
		 * @return 
		 */		
		return current; 
	}
	
	void runOnCurrent() {
		/**
		 * @brief This is called by the constructor to compute the posterior. NOTE it does not callback
		 */
		
		std::lock_guard guard(current_mutex);
		current.compute_posterior(*data);
		// NOTE: We do NOT count this as a "sample" since it is not yielded
	}
	
	
	const HYP& getMax() { 
		return maxval; 
	} 
	
	void restart() { 
		
		current = current.restart();
		current.compute_posterior(*data);
		
		steps_since_improvement = 0; // reset the couter
		maxval = current.posterior; // and the new max
	}
	
	/**
	 * @brief This allows us to overwrite/enforce stuff about proposals in subclasses of MCMCChain
	 * @param p
	 * @return 
	 */	
	virtual bool check(HYP& p) {
		return true; 
	}
	
	/**
	 * @brief Run MCMC according to the control parameters passed in.
	 * 		  NOTE: ctl cannot be passed by reference. 
	 * @param ctl
	 */	
	 generator<HYP&> run(Control ctl) {

		assert(ctl.nthreads == 1 && "*** You seem to have called MCMCChain with nthreads>1. This is not how you parallel. Check out ChainPool"); 
		
		#ifdef DEBUG_MCMC
			DEBUG("# Starting MCMC Chain on\t", current.posterior, current.prior, current.likelihood, current.string());
		#endif 
		
		// I may have copied its start time from somewhere else, so change that here
		ctl.start();		
		while(true) {
			
			if(not ctl.running()) 
				break;
			
			std::lock_guard guard(current_mutex);
			
			if(current.posterior > maxval) { // if we improve, store it
				maxval = current.posterior;
				steps_since_improvement = 0;
			}
			else { // else keep track of how long
				++steps_since_improvement;
			}
			
			// if we haven't improved
			if(ctl.restart>0 and steps_since_improvement > ctl.restart){
				[[unlikely]];
				restart();
				print("RESTARTING (from no improvement)", current.string());
			}
			else if (std::isnan(current.posterior) or std::isinf(current.posterior)) { // either inf is a restart
				[[unlikely]];
				print("RESTARTING (from -inf)", current.string());
				// This is a special case where we just propose from restarting 
				restart();

				// Should we count in history? 	// Hmm maybe not. 
			}
			else {
				// normally we go here and do a proper proposal
				
				#ifdef DEBUG_MCMC
				DEBUG("# Current", current.posterior, current.prior, current.likelihood, current.string());
				#endif 
				
				// propose, but restart if we're -infinity
				auto p = current.propose();
				if(not p) { continue;  }// proposal failed
					
				auto [proposal, fb] = p.value();			
				
				++proposals;
				
				// A lot of proposals end up with the same function, so if so, save time by not
				// computing the posterior
				if(proposal == current) {
					// copy all the properties
					// NOTE: This is necessary because == might just check value, but operator= will copy everything else
					proposal = current; 
				
					// we treat this as an accept
					history << true; 
					++acceptances;		

					#ifdef DEBUG_MCMC
					// they are equal but we just use current here
					DEBUG("# Proposed(eq)", current.posterior, current.prior, current.likelihood, current.string(), "fb="+str(fb));
					#endif 
					
					if(not FleetArgs::MCMCYieldOnlyChanges) {
						co_yield current; // must be done with lock
					}
				}
				else {
					
					// we add a subroutine "check" here that can reject proposals right away
					// this is useful for enforcing some constraints on the proposals
					// defaultly, check does nothing. NOTE: it is important to the shibbholeth sampler that
					// this happens before we compute posteriors
					if(not check(proposal)) {						
						history << false;						
						continue;
					}
										
					
					// here we actually need to compute, but we can do so at the breakout
					// TODO: This is a little inefficient in that we compute log(uniform()) even
					// when we are special (and it is thus unused)
					const double u = log(uniform());
									
					// NOTE: The above is NOT right because the prior is not at temperature, so
					// instead of multiplying by temperature we have to do something smarter to fix the fact that
					// its only on the likelihood. Reverting now to breakout=-infinity but keeping the rest of code in place
					// for when this is fixed
//					const auto breakoutpair = std::make_pair(-infinity, 1.0);
					
					// ok we will accept if u < proposal.at_temperature(temperature) - current.at_temperature(temperature) - fb;
					// or u + current.at_temperature(temperature) + fb < proposal.at_temperature(temperature)
					// or (u + current.at_temperature(temperature) + fb - PRIOR)*temperature < LIKELIHOOD
					// NOTE then that in compute_posterior and compute_likelihood, we must NOT take into 
					// account tempearture
					// NOTE: This breakout is on *posteriors* but in compute_posterior it is converted to one 
					// on likelihoods for compute_likelihood
					const auto breakoutpair = std::make_pair(u + current.at_temperature(temperature) + fb, (double)temperature);
					
					proposal.compute_posterior(*data, breakoutpair);
//					proposal.compute_posterior(*data);
					
//					#ifdef DEBUG_MCMC
//					DEBUG("# Proposed", proposal.posterior, proposal.prior, proposal.likelihood, proposal.string(), "fb="+str(fb));
//					#endif
					if(FleetArgs::print_proposals != 0) [[unlikely]] {
						print("#Proposed", proposal.posterior, proposal.prior, proposal.likelihood, proposal.string(), "fb="+str(fb));
					}
					
					const double ratio = proposal.at_temperature(temperature) - current.at_temperature(temperature) - fb;
					
					// this is just a little debugging/checking code to see that we are making the same decision as 
					// without breakout. It should be commented out unless we're check
//					assert( u < ratio == proposal.at_temperature(temperature) - current.at_temperature(temperature) - fb

					if((not std::isnan(proposal.posterior)) and u < ratio) {					
						[[unlikely]];
									
						#ifdef DEBUG_MCMC
							DEBUG("# ACCEPT");
						#endif 
						
						current = std::move(proposal);
		  
						history << true;
						++acceptances;
						
						// we always yield accepts
						co_yield current; // must be done with lock
					}
					else {
						history << false;
						
						#ifdef DEBUG_MCMC
							DEBUG("# REJECT");
						#endif 
						
						// only yield rejects when not MCMCYieldOnlyChanges 
						if(not FleetArgs::MCMCYieldOnlyChanges) {
							co_yield current; 
						}
					}
				
					
				}				
			}
			
			++samples;			
			++FleetStatistics::global_sample_count;
			
			
			
		}
	}
	
	void run() { 
		/**
		 * @brief Run forever
		 */
		run(Control(0,0)); 
	}

	double acceptance_ratio() {
		/**
		 * @brief Get my acceptance ratio
		 * @return 
		 */
		return history.mean();
	}
	
	double at_temperature(double t){
		/**
		 * @brief Return my current posterior at a given temperature t
		 * @param t
		 * @return 
		 */
		return current.at_temperature(t);
	}
	
};
