"""
Advanced agent manager with MCP and cloud-native capabilities.
"""
from src.agent.base import Agent, Skill
import src.agent.skills as skills
import src.agent.cloud_skills as cloud_skills
import src.agent.mcp_integration as mcp
import src.agent.intelligence_orchestrator as intelligence


class CloudArchitectAgent(Agent):
    """Advanced agent for cloud-native architecture and blueprint generation."""
    
    def __init__(self):
        super().__init__(
            name="CloudArchitect",
            persona="You are an elite cloud-native architect specializing in Kubernetes, "
                   "microservices, and infrastructure as code. You generate production-ready "
                   "blueprints following best practices."
        )
        self._load_skills()
    
    def _load_skills(self):
        """Load cloud-native skills."""
        self.add_skill(Skill.from_callable(cloud_skills.generate_kubernetes_deployment))
        self.add_skill(Skill.from_callable(cloud_skills.generate_docker_compose))
        self.add_skill(Skill.from_callable(cloud_skills.generate_terraform_module))
        self.add_skill(Skill.from_callable(cloud_skills.generate_github_actions_pipeline))
        self.add_skill(Skill.from_callable(cloud_skills.generate_monitoring_stack))
        self.add_skill(Skill.from_callable(cloud_skills.estimate_cloud_costs))
    
    def run(self, user_input: str) -> str:
        """Enhanced command dispatcher for cloud architecture."""
        args = user_input.split()
        if not args:
            return "Please provide a cloud architecture command."
        
        command = args[0].lower()
        
        if command in ["k8s", "kubernetes"]:
            if len(args) < 3:
                return "Usage: k8s <app_name> <image>"
            app_name, image = args[1], args[2]
            return self.get_skill("generate_kubernetes_deployment")(app_name, image)
        
        elif command in ["docker", "compose"]:
            return self.get_skill("generate_docker_compose")([
                {"name": "app", "image": "nginx:latest", "ports": ["8080:80"]}
            ])
        
        elif command == "terraform":
            if len(args) < 2:
                return "Usage: terraform <resource_type>"
            resource_type = args[1]
            return self.get_skill("generate_terraform_module")(
                "aws", resource_type, "my_resource", {}
            )
        
        elif command in ["cicd", "pipeline"]:
            if len(args) < 2:
                return "Usage: cicd <app_name>"
            return self.get_skill("generate_github_actions_pipeline")(args[1], [])
        
        elif command == "monitoring":
            return self.get_skill("generate_monitoring_stack")()
        
        elif command in ["cost", "estimate"]:
            return str(self.get_skill("estimate_cloud_costs")([
                {"type": "t3.medium", "quantity": 2, "name": "web-servers"}
            ]))
        
        elif command in ["help", "?"]:
            return self.list_skills()
        
        else:
            return f"Unknown command '{command}'. Try 'help' for available commands."


class MCPIntegrationAgent(Agent):
    """Agent for MCP server integration."""
    
    def __init__(self):
        super().__init__(
            name="MCPIntegrator",
            persona="You are an MCP integration specialist. You connect to MCP servers "
                   "and leverage their resources, tools, and prompts for enhanced capabilities."
        )
        self._load_skills()
    
    def _load_skills(self):
        """Load MCP skills."""
        self.add_skill(Skill.from_callable(mcp.connect_mcp_server))
        self.add_skill(Skill.from_callable(mcp.list_mcp_resources))
        self.add_skill(Skill.from_callable(mcp.read_mcp_resource))
        self.add_skill(Skill.from_callable(mcp.invoke_mcp_tool))
        self.add_skill(Skill.from_callable(mcp.get_mcp_prompt))
        self.add_skill(Skill.from_callable(mcp.mcp_server_status))
    
    def run(self, user_input: str) -> str:
        """Command dispatcher for MCP operations."""
        args = user_input.split()
        if not args:
            return "Please provide an MCP command."
        
        command = args[0].lower()
        
        if command == "connect":
            if len(args) < 3:
                return "Usage: connect <name> <url>"
            return self.get_skill("connect_mcp_server")(args[1], args[2])
        
        elif command in ["list", "resources"]:
            return self.get_skill("list_mcp_resources")()
        
        elif command == "read":
            if len(args) < 2:
                return "Usage: read <uri>"
            return self.get_skill("read_mcp_resource")(args[1])
        
        elif command == "tool":
            if len(args) < 3:
                return "Usage: tool <server> <tool_name>"
            return self.get_skill("invoke_mcp_tool")(args[1], args[2])
        
        elif command == "status":
            return self.get_skill("mcp_server_status")()
        
        elif command in ["help", "?"]:
            return self.list_skills()
        
        else:
            return f"Unknown command '{command}'. Try 'help'."


class IntelligenceOrchestratorAgent(Agent):
    """Agent for orchestrating reusable intelligence."""
    
    def __init__(self):
        super().__init__(
            name="IntelligenceOrchestrator",
            persona="You are a master intelligence orchestrator. You manage patterns, "
                   "compose skills, and coordinate multi-agent workflows."
        )
        self._load_skills()
    
    def _load_skills(self):
        """Load intelligence orchestration skills."""
        self.add_skill(Skill.from_callable(intelligence.create_intelligence_pattern))
        self.add_skill(Skill.from_callable(intelligence.list_intelligence_patterns))
        self.add_skill(Skill.from_callable(intelligence.compose_agent_skills))
        self.add_skill(Skill.from_callable(intelligence.share_agent_context))
        self.add_skill(Skill.from_callable(intelligence.store_intelligence))
        self.add_skill(Skill.from_callable(intelligence.retrieve_intelligence))
        self.add_skill(Skill.from_callable(intelligence.get_intelligence_summary))
    
    def run(self, user_input: str) -> str:
        """Command dispatcher for intelligence orchestration."""
        args = user_input.split()
        if not args:
            return "Please provide an orchestration command."
        
        command = args[0].lower()
        
        if command in ["patterns", "list"]:
            return self.get_skill("list_intelligence_patterns")()
        
        elif command == "compose":
            if len(args) < 3:
                return "Usage: compose <skill1,skill2,...> <workflow_name>"
            skills_list = args[1].split(',')
            return self.get_skill("compose_agent_skills")(skills_list, args[2])
        
        elif command == "summary":
            return self.get_skill("get_intelligence_summary")()
        
        elif command in ["help", "?"]:
            return self.list_skills()
        
        else:
            return f"Unknown command '{command}'. Try 'help'."
