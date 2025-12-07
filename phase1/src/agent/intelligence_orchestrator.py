"""
Reusable intelligence patterns and skill composition framework.
Enables agents to combine skills and share knowledge.
"""
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
import json


@dataclass
class IntelligencePattern:
    """Represents a reusable intelligence pattern."""
    name: str
    description: str
    skills: List[str]  # Skill names in order
    context_template: Dict[str, Any]
    success_criteria: List[str]
    
    def execute(self, agent, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the intelligence pattern."""
        context = {**self.context_template, **initial_context}
        results = []
        
        for skill_name in self.skills:
            skill = agent.get_skill(skill_name)
            if skill:
                result = skill(**context)
                results.append(result)
                context['previous_result'] = result
        
        return {
            "pattern": self.name,
            "results": results,
            "context": context,
            "success": True
        }


class IntelligenceOrchestrator:
    """
    Orchestrates multi-agent workflows and manages reusable intelligence.
    """
    
    def __init__(self):
        self.patterns: Dict[str, IntelligencePattern] = {}
        self.knowledge_base: Dict[str, Any] = {}
        self._load_default_patterns()
    
    def _load_default_patterns(self):
        """Load default intelligence patterns."""
        # Research & Synthesize pattern
        self.patterns["research_synthesize"] = IntelligencePattern(
            name="research_synthesize",
            description="Gather information, analyze, and summarize",
            skills=["search_tasks", "get_statistics", "list_tasks"],
            context_template={"mode": "research"},
            success_criteria=["data_gathered", "analysis_complete", "summary_generated"]
        )
        
        # Plan & Execute pattern
        self.patterns["plan_execute"] = IntelligencePattern(
            name="plan_execute",
            description="Break down task, sequence steps, implement",
            skills=["search_tasks", "add_task", "update_task"],
            context_template={"mode": "execution"},
            success_criteria=["plan_created", "steps_sequenced", "execution_started"]
        )
    
    def register_pattern(self, pattern: IntelligencePattern):
        """Register a new intelligence pattern."""
        self.patterns[pattern.name] = pattern
    
    def get_pattern(self, name: str) -> Optional[IntelligencePattern]:
        """Get an intelligence pattern by name."""
        return self.patterns.get(name)
    
    def list_patterns(self) -> str:
        """List all available intelligence patterns."""
        if not self.patterns:
            return "No intelligence patterns available"
        
        output = ["Available Intelligence Patterns:\n"]
        for name, pattern in self.patterns.items():
            output.append(f"📋 {name}")
            output.append(f"   {pattern.description}")
            output.append(f"   Skills: {', '.join(pattern.skills)}")
            output.append("")
        
        return "\n".join(output)
    
    def compose_skills(self, skill_names: List[str], workflow_name: str) -> str:
        """
        Compose multiple skills into a workflow.
        
        Args:
            skill_names: List of skill names to compose
            workflow_name: Name for the composed workflow
            
        Returns:
            Composition result
        """
        workflow = {
            "name": workflow_name,
            "skills": skill_names,
            "type": "sequential",
            "created": "2025-12-07"
        }
        
        self.knowledge_base[f"workflow_{workflow_name}"] = workflow
        
        return f"""✓ Created workflow '{workflow_name}'
Skills: {' → '.join(skill_names)}
Type: Sequential execution
Saved to knowledge base
"""
    
    def share_context(self, agent_from: str, agent_to: str, context: Dict[str, Any]) -> str:
        """
        Share context between agents.
        
        Args:
            agent_from: Source agent name
            agent_to: Target agent name
            context: Context to share
            
        Returns:
            Status message
        """
        key = f"context_{agent_from}_to_{agent_to}"
        self.knowledge_base[key] = {
            "from": agent_from,
            "to": agent_to,
            "context": context,
            "timestamp": "2025-12-07T22:00:00Z"
        }
        
        return f"✓ Context shared from {agent_from} to {agent_to}\n" \
               f"  Keys: {', '.join(context.keys())}"
    
    def store_knowledge(self, key: str, value: Any) -> str:
        """Store knowledge in the knowledge base."""
        self.knowledge_base[key] = value
        return f"✓ Stored knowledge: {key}"
    
    def retrieve_knowledge(self, key: str) -> Any:
        """Retrieve knowledge from the knowledge base."""
        return self.knowledge_base.get(key)
    
    def get_knowledge_summary(self) -> str:
        """Get summary of knowledge base."""
        if not self.knowledge_base:
            return "Knowledge base is empty"
        
        output = ["Knowledge Base Summary:\n"]
        for key, value in self.knowledge_base.items():
            if isinstance(value, dict):
                output.append(f"📚 {key}: {len(value)} items")
            else:
                output.append(f"📚 {key}: {type(value).__name__}")
        
        output.append(f"\nTotal entries: {len(self.knowledge_base)}")
        return "\n".join(output)


# Global orchestrator instance
orchestrator = IntelligenceOrchestrator()


# Skill functions
def create_intelligence_pattern(name: str, description: str, skills: List[str]) -> str:
    """Create a new intelligence pattern."""
    pattern = IntelligencePattern(
        name=name,
        description=description,
        skills=skills,
        context_template={},
        success_criteria=[]
    )
    orchestrator.register_pattern(pattern)
    return f"✓ Created intelligence pattern '{name}'\nSkills: {', '.join(skills)}"


def list_intelligence_patterns() -> str:
    """List all intelligence patterns."""
    return orchestrator.list_patterns()


def compose_agent_skills(skill_names: List[str], workflow_name: str) -> str:
    """Compose skills into a workflow."""
    return orchestrator.compose_skills(skill_names, workflow_name)


def share_agent_context(agent_from: str, agent_to: str, context_data: Dict[str, Any]) -> str:
    """Share context between agents."""
    return orchestrator.share_context(agent_from, agent_to, context_data)


def store_intelligence(key: str, value: Any) -> str:
    """Store intelligence in knowledge base."""
    return orchestrator.store_knowledge(key, value)


def retrieve_intelligence(key: str) -> Any:
    """Retrieve intelligence from knowledge base."""
    return orchestrator.retrieve_knowledge(key)


def get_intelligence_summary() -> str:
    """Get intelligence summary."""
    return orchestrator.get_knowledge_summary()
