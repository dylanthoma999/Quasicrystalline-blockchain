"""
Agent-Based Model (ABM) for Quasicrystalline Governance
=========================================================

Simulates decentralized DAO governance with parastatistic transitions.
Maps p-parameter (order of parastatistics) to governance modes:
  - Low p (1-5): Collective quorum mode, high coordination
  - Medium p (5-50): Mixed mode
  - High p (50-100+): Autonomous Maxwell-Boltzmann mode

Author: Raccoon AI
Date: 2026-07-14
"""
import json
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime


@dataclass
class ProposalVote:
    """Represents a governance proposal vote."""
    proposal_id: int
    creator: int
    description: str
    creation_time: float
    yes_votes: int = 0
    no_votes: int = 0
    abstain_votes: int = 0
    status: str = "active"  # active, passed, rejected, expired
    quorum_threshold: float = 0.51


@dataclass
class AgentState:
    """Internal state of a governance agent."""
    agent_id: int
    grading_sector: Tuple[int, int]  # (a, b) in Z_2 x Z_2
    voting_power: float
    cognitive_load: float  # 0-1, impacts decision-making
    last_vote_time: float
    trust_scores: Dict[int, float]  # trust in other agents
    alignment: float  # -1 to 1, policy alignment
    autonomy_preference: float  # 0-1, preference for independent decisions


class QuasicrystallineGovernanceABM:
    """
    Agent-Based Model for parastatistic-driven governance.
    """
    
    def __init__(
        self,
        n_agents: int = 50,
        p_initial: float = 5.0,
        time_horizon: int = 1000,
        seed: int = 42,
    ):
        """
        Initialize the governance ABM.
        
        Args:
            n_agents: Number of agents (DAO members)
            p_initial: Initial parastatistics order
            time_horizon: Number of time steps to simulate
            seed: Random seed for reproducibility
        """
        self.n_agents = n_agents
        self.p_current = p_initial
        self.p_history = [p_initial]
        self.time_horizon = time_horizon
        self.current_time = 0.0
        self.dt = 1.0
        
        np.random.seed(seed)
        
        # Initialize agents
        self.agents: List[AgentState] = []
        self._initialize_agents()
        
        # Governance state
        self.proposals: Dict[int, ProposalVote] = {}
        self.proposal_counter = 0
        self.active_proposals: List[int] = []
        
        # Metrics
        self.metrics = {
            'convergence_time': [],
            'proposal_passage_rate': [],
            'autonomy_ratio': [],
            'coordination_efficiency': [],
            'consensus_strength': [],
            'p_parameter': [],
            'collective_trust': [],
            'decision_latency': [],
        }
        
    def _initialize_agents(self):
        """Initialize agents with grading sectors and preferences."""
        for i in range(self.n_agents):
            a_sector = np.random.randint(0, 2)
            b_sector = np.random.randint(0, 2)
            
            agent = AgentState(
                agent_id=i,
                grading_sector=(a_sector, b_sector),
                voting_power=np.random.uniform(0.5, 2.0),
                cognitive_load=np.random.uniform(0.0, 0.3),
                last_vote_time=0.0,
                trust_scores={j: np.random.uniform(0.3, 1.0) for j in range(self.n_agents)},
                alignment=np.random.uniform(-1.0, 1.0),
                autonomy_preference=np.random.uniform(0.0, 1.0),
            )
            self.agents.append(agent)
    
    def _compute_parastatistic_phase(self) -> float:
        """
        Compute phase of R-matrix based on p and current conditions.
        θ_p = π(p-1)/(2p) - phase of exchange statistics
        """
        if self.p_current < 1:
            return 0.0
        phi_p = np.pi * (self.p_current - 1) / (2 * self.p_current)
        return phi_p
    
    def _agent_decision_threshold(self, agent: AgentState) -> float:
        """
        Compute voting threshold for an agent based on p-parameter.
        
        Low p: High threshold (need strong consensus)
        High p: Low threshold (more independent)
        """
        phi_p = self._compute_parastatistic_phase()
        
        # Base threshold modified by p and autonomy preference
        base_threshold = 0.5 + 0.2 * np.sin(phi_p)
        autonomy_adjustment = agent.autonomy_preference * (1.0 - 1.0 / self.p_current)
        cognitive_penalty = agent.cognitive_load * 0.2
        
        threshold = np.clip(base_threshold + autonomy_adjustment - cognitive_penalty, 0.3, 0.7)
        return threshold
    
    def _collective_trust_metric(self) -> float:
        """Compute average trust across all agents (collective coherence)."""
        total_trust = 0.0
        count = 0
        for agent in self.agents:
            for trust_val in agent.trust_scores.values():
                total_trust += trust_val
                count += 1
        return total_trust / count if count > 0 else 0.5
    
    def _coordination_efficiency(self) -> float:
        """Measure how well agents coordinate (reduce variance in votes)."""
        alignments = [agent.alignment for agent in self.agents]
        if len(alignments) > 1:
            variance = np.var(alignments)
            efficiency = 1.0 / (1.0 + variance)
        else:
            efficiency = 0.5
        return float(efficiency)
    
    def _autonomy_ratio(self) -> float:
        """Measure how autonomous agents have become (p → ∞)."""
        if self.p_current < 1:
            return 0.0
        autonomy = min(1.0, (self.p_current - 1.0) / 100.0)
        return autonomy
    
    def create_proposal(self, time: float) -> int:
        """Create a new governance proposal."""
        prop_id = self.proposal_counter
        self.proposal_counter += 1
        
        creator = np.random.randint(0, self.n_agents)
        proposal = ProposalVote(
            proposal_id=prop_id,
            creator=creator,
            description=f"Proposal {prop_id} from agent {creator}",
            creation_time=time,
        )
        self.proposals[prop_id] = proposal
        self.active_proposals.append(prop_id)
        return prop_id
    
    def agent_vote(self, agent_id: int, proposal_id: int, time: float) -> bool:
        """Agent casts a vote on a proposal."""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        if proposal.status != "active":
            return False
        
        agent = self.agents[agent_id]
        threshold = self._agent_decision_threshold(agent)
        
        # Decision: vote yes with probability based on trust and alignment
        vote_prob = agent.trust_scores[proposal.creator] * (0.5 + 0.5 * agent.alignment)
        vote_yes = np.random.random() < vote_prob
        
        if vote_yes:
            proposal.yes_votes += int(agent.voting_power)
        else:
            proposal.no_votes += int(agent.voting_power)
        
        agent.last_vote_time = time
        return True
    
    def finalize_proposal(self, prop_id: int, time: float) -> str:
        """Finalize a proposal (check passage, mark as expired, etc.)."""
        if prop_id not in self.proposals:
            return "unknown"
        
        proposal = self.proposals[prop_id]
        total_votes = proposal.yes_votes + proposal.no_votes
        
        # Check quorum
        total_power = sum(agent.voting_power for agent in self.agents)
        if total_votes < proposal.quorum_threshold * total_power:
            proposal.status = "expired"
            return "expired"
        
        # Check passage
        passage_rate = proposal.yes_votes / total_votes if total_votes > 0 else 0.0
        if passage_rate > 0.5:
            proposal.status = "passed"
            return "passed"
        else:
            proposal.status = "rejected"
            return "rejected"
    
    def update_p_parameter(self, time: float):
        """Update p based on governance dynamics and elapsed time."""
        # p increases linearly with time (transition from collective to autonomous)
        time_scale = self.time_horizon / 100.0
        p_increment = 0.95 / time_scale
        self.p_current += p_increment
        self.p_history.append(self.p_current)
    
    def step(self):
        """Execute one time step of the simulation."""
        # Create proposals with some probability
        if np.random.random() < 0.15:
            self.create_proposal(self.current_time)
        
        # Agents vote on active proposals
        for prop_id in self.active_proposals[:]:
            for agent_id in range(self.n_agents):
                if np.random.random() < 0.3:  # 30% participation rate
                    self.agent_vote(agent_id, prop_id, self.current_time)
        
        # Finalize proposals that have been active long enough
        for prop_id in self.active_proposals[:]:
            if self.proposals[prop_id].status != "active":
                self.active_proposals.remove(prop_id)
        
        # Update p parameter
        self.update_p_parameter(self.current_time)
        
        # Record metrics
        self._record_metrics()
        
        self.current_time += self.dt
    
    def _record_metrics(self):
        """Record current state metrics."""
        self.metrics['collective_trust'].append(self._collective_trust_metric())
        self.metrics['coordination_efficiency'].append(self._coordination_efficiency())
        self.metrics['autonomy_ratio'].append(self._autonomy_ratio())
        self.metrics['p_parameter'].append(self.p_current)
    
    def run_simulation(self) -> Dict:
        """Run the full simulation."""
        for step_num in range(self.time_horizon):
            self.step()
        
        return self._compile_results()
    
    def _compile_results(self) -> Dict:
        """Compile simulation results into a dictionary."""
        total_proposals = len(self.proposals)
        proposals_passed = sum(1 for p in self.proposals.values() if p.status == "passed")
        proposals_rejected = sum(1 for p in self.proposals.values() if p.status == "rejected")
        proposals_expired = sum(1 for p in self.proposals.values() if p.status == "expired")
        
        passage_rate = proposals_passed / total_proposals if total_proposals > 0 else 0.0
        
        return {
            'n_agents': self.n_agents,
            'time_horizon': self.time_horizon,
            'initial_p': self.p_history[0],
            'final_p': self.p_history[-1],
            'p_history': self.p_history,
            'total_proposals': total_proposals,
            'proposals_passed': proposals_passed,
            'proposals_rejected': proposals_rejected,
            'proposals_expired': proposals_expired,
            'passage_rate': passage_rate,
            'metrics': self.metrics,
            'timestamp': str(datetime.now()),
        }
    
    def plot_results(self, save_path: str = "abm_governance_results.png"):
        """Plot simulation results."""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        time_steps = range(len(self.metrics['p_parameter']))
        
        # p-parameter evolution
        axes[0, 0].plot(time_steps, self.metrics['p_parameter'], linewidth=2, color='blue')
        axes[0, 0].axhline(y=50, color='r', linestyle='--', label='Classical→Bosonic')
        axes[0, 0].set_title('Evolution of p-Parameter')
        axes[0, 0].set_xlabel('Time Step')
        axes[0, 0].set_ylabel('p-parameter')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Collective trust
        axes[0, 1].fill_between(time_steps, self.metrics['collective_trust'], alpha=0.5, color='orange')
        axes[0, 1].set_title('Inter-Agent Trust Evolution')
        axes[0, 1].set_xlabel('Time Step')
        axes[0, 1].set_ylabel('Collective Trust [0-1]')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Coordination efficiency
        axes[0, 2].fill_between(time_steps, self.metrics['coordination_efficiency'], alpha=0.5, color='green')
        axes[0, 2].set_title('Coordination Efficiency')
        axes[0, 2].set_xlabel('Time Step')
        axes[0, 2].set_ylabel('Efficiency [0-1]')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Autonomy ratio
        axes[1, 0].fill_between(time_steps, self.metrics['autonomy_ratio'], alpha=0.5, color='red')
        axes[1, 0].set_title('Autonomy Ratio')
        axes[1, 0].set_xlabel('Time Step')
        axes[1, 0].set_ylabel('Autonomy Ratio')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Phase space: p vs Efficiency
        axes[1, 1].scatter(self.metrics['p_parameter'], self.metrics['coordination_efficiency'], 
                          c=time_steps, cmap='viridis', s=20, alpha=0.6)
        axes[1, 1].set_title('Phase Space: p vs Efficiency')
        axes[1, 1].set_xlabel('p-parameter')
        axes[1, 1].set_ylabel('Coordination Efficiency')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Proposal outcomes
        results = self._compile_results()
        labels = ['Passed', 'Rejected']
        sizes = [results['proposals_passed'], results['proposals_rejected']]
        colors = ['green', 'red']
        axes[1, 2].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        axes[1, 2].set_title('Proposal Outcomes')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()


def run_governance_simulation():
    """Run a complete governance ABM simulation."""
    # Create and run simulation
    abm = QuasicrystallineGovernanceABM(
        n_agents=75,
        p_initial=5.0,
        time_horizon=1000,
        seed=42,
    )
    
    results = abm.run_simulation()
    
    # Save results
    results_json = json.dumps(results, indent=2, default=str)
    with open('abm_governance_results.json', 'w') as f:
        f.write(results_json)
    
    # Plot results
    abm.plot_results()
    
    # Print summary
    print("\n" + "="*60)
    print("GOVERNANCE ABM SIMULATION RESULTS")
    print("="*60)
    print(f"Total Agents: {results['n_agents']}")
    print(f"Simulation Time Steps: {results['time_horizon']}")
    print(f"Initial p-parameter: {results['initial_p']:.2f}")
    print(f"Final p-parameter: {results['final_p']:.2f}")
    print(f"Total Proposals: {results['total_proposals']}")
    print(f"  - Passed: {results['proposals_passed']}")
    print(f"  - Rejected: {results['proposals_rejected']}")
    print(f"  - Expired: {results['proposals_expired']}")
    print(f"Overall Passage Rate: {results['passage_rate']:.1%}")
    print(f"\nFinal Metrics:")
    print(f"  - Collective Trust: {results['metrics']['collective_trust'][-1]:.3f}")
    print(f"  - Coordination Efficiency: {results['metrics']['coordination_efficiency'][-1]:.3f}")
    print(f"  - Autonomy Ratio: {results['metrics']['autonomy_ratio'][-1]:.3f}")
    print("="*60)
    
    return results, abm


if __name__ == "__main__":
    results, abm = run_governance_simulation()
