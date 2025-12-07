import pytest
from src.agent.base import Agent, Skill

def sample_function(x: int, y: int = 10) -> int:
    """Adds two numbers."""
    return x + y

def test_skill_creation_from_callable():
    skill = Skill.from_callable(sample_function)
    assert skill.name == "sample_function"
    assert skill.description == "Adds two numbers."
    assert skill.parameters['x'] == "int"
    assert skill.parameters['y'] == "int"
    assert skill(5, y=5) == 10

def test_agent_initialization():
    agent = Agent(name="TestBot", persona="Testing")
    assert agent.name == "TestBot"
    assert agent.persona == "Testing"
    assert agent.skills == []

def test_agent_add_and_get_skill():
    agent = Agent(name="TestBot", persona="Testing")
    skill = Skill.from_callable(sample_function)
    agent.add_skill(skill)
    
    assert len(agent.skills) == 1
    assert agent.get_skill("sample_function") == skill
    assert agent.get_skill("non_existent") is None

def test_agent_list_skills():
    agent = Agent(name="TestBot", persona="Testing")
    skill = Skill.from_callable(sample_function)
    agent.add_skill(skill)
    
    listing = agent.list_skills()
    assert "sample_function" in listing
    assert "x: int" in listing
    assert "y: int" in listing

def test_agent_run_not_implemented():
    agent = Agent(name="TestBot", persona="Testing")
    with pytest.raises(NotImplementedError):
        agent.run("hello")
