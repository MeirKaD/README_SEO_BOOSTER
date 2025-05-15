from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os
from typing import List, Tuple, Dict, Any
import json


@CrewBase
class ReadmeSeoBooster():
    """Crew for boosting SEO of GitHub README files"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        """Initialize the crew with necessary tools"""
        self._init_mcp_tools()
        
        self.github_tool = getattr(self, 'github_tool', None)
        self.brightdata_tool = getattr(self, 'brightdata_tool', None)
        
        super().__init__()
    def _find_first_paragraph_end(self, lines: List[str]) -> int:
        """Find the end line of the first paragraph."""
        in_paragraph = False
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and not in_paragraph:
                in_paragraph = True
            elif not line.strip() and in_paragraph:
                return i
        return len(lines)
    
    def validate_readme_changes(self, result) -> Tuple[bool, Any]:
        """Validate that only the first paragraph has been modified."""
        try:
            if hasattr(result, 'json_dict') and result.json_dict:
                data = result.json_dict
            elif hasattr(result, 'raw'):
                try:
                    data = json.loads(result.raw)
                except:
                    return (False, "Could not parse result as JSON")
            else:
                return (False, "Result has no json_dict or raw attribute")
                
            updated_readme = data.get("updated_readme", "")
            
            original_readme = self.get_original_readme()
            
            if not original_readme or not updated_readme:
                return (False, "Missing original or updated README content")
            
            updated_lines = updated_readme.strip().split('\n')
            original_lines = original_readme.strip().split('\n')
            
            first_para_end_original = self._find_first_paragraph_end(original_lines)
            first_para_end_updated = self._find_first_paragraph_end(updated_lines)
            
            if abs(len(updated_lines) - len(original_lines)) > 20:
                return (False, "The updated README's length is significantly different from the original")
            
            if len(original_lines) > first_para_end_original and len(updated_lines) > first_para_end_updated:
                for i in range(first_para_end_original, min(len(original_lines), len(updated_lines))):
                    orig_index = i
                    updated_index = i + (first_para_end_updated - first_para_end_original)
                    
                    if updated_index >= len(updated_lines):
                        break
                        
                    if original_lines[orig_index] != updated_lines[updated_index]:
                        return (False, f"Content beyond the first paragraph has been modified at line {i}")
            
            return (True, result)
        except Exception as e:
            return (False, f"Error validating README changes: {str(e)}")
    def _init_mcp_tools(self):
        """Initialize MCP tools for Bright Data and GitHub"""
        # Bright Data MCP setup
        try:
            brightdata_params = StdioServerParameters(
                command="npx",
                args=["@brightdata/mcp"],
                env={
                    "API_TOKEN": os.getenv("BRIGHTDATA_API_TOKEN"),
                    "WEB_UNLOCKER_ZONE": "unblocker"
                }
            )
            self.brightdata_adapter = MCPServerAdapter(brightdata_params)
            self.brightdata_tool = self.brightdata_adapter.tools[0]
        except Exception as e:
            print(f"Error initializing Bright Data MCP: {e}")
            self.brightdata_tool = None
        
        # GitHub MCP setup
        try:
            github_params = StdioServerParameters(
                command="docker",
                args=[
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "ghcr.io/github/github-mcp-server"
                ],
                env={
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PAT"),
                    "GITHUB_TOOLSETS": "repos,pull_requests" 
                }
            )
            self.github_adapter = MCPServerAdapter(github_params)
            self.github_tools = self.github_adapter.tools
            print(f"Available GitHub tools ({len(self.github_tools)}):")
            for i, tool in enumerate(self.github_tools):
                print(f"  {i+1}. {tool.name}")
            self.github_tool = self.github_tools[0] if self.github_tools else None
        except Exception as e:
            print(f"Error initializing GitHub MCP: {e}")
            self.github_tool = self._create_github_tool()  # Fallback to original GitHub tool if MCP fails
    @agent
    def keyword_miner(self) -> Agent:
        """Agent for mining SEO keywords"""
        return Agent(
            config=self.agents_config['keyword_miner'],
            verbose=True,
            tools=[self.brightdata_tool] if self.brightdata_tool else []
        )

    @agent
    def seo_refiner(self) -> Agent:
        """Agent for refining README content with keywords"""
        pr_tools = []
        tool_names = [
            "list_branches",
            "create_branch",
            "get_file_contents",
            "create_or_update_file",
            "push_files",
            "create_pull_request"
        ]
        
        if hasattr(self, 'github_tools') and self.github_tools:
            for name in tool_names:
                matching_tools = [tool for tool in self.github_tools if name.lower() in tool.name.lower()]
                if matching_tools:
                    pr_tools.extend(matching_tools)
            
            print(f"PR Bot will use {len(pr_tools)} tools:")
            for i, tool in enumerate(pr_tools):
                print(f"  {i+1}. {tool.name}")
        return Agent(
            config=self.agents_config['seo_refiner'],
            verbose=True,
            tools=pr_tools
        )
    
    @agent
    def pr_bot(self) -> Agent:
        """Agent for creating pull requests"""
        pr_tools = []
        tool_names = [
            "list_branches",
            "create_branch",
            "get_file_contents",
            "create_or_update_file",
            "push_files",
            "create_pull_request"
        ]
        
        if hasattr(self, 'github_tools') and self.github_tools:
            for name in tool_names:
                matching_tools = [tool for tool in self.github_tools if name.lower() in tool.name.lower()]
                if matching_tools:
                    pr_tools.extend(matching_tools)
            
            print(f"PR Bot will use {len(pr_tools)} tools:")
            for i, tool in enumerate(pr_tools):
                print(f"  {i+1}. {tool.name}")
            
            return Agent(
                config=self.agents_config['pr_bot'],
                verbose=True,
                tools=pr_tools
            )
        else:
            return Agent(
                config=self.agents_config['pr_bot'],
                verbose=True,
                tools=[self.github_tool] if self.github_tool else []
            )
    
    @task
    def mine_keywords_task(self) -> Task:
        """Task for mining keywords"""
        return Task(
            config=self.tasks_config['mine_keywords_task']
        )

    @task
    def refine_readme_task(self) -> Task:
        """Task for refining README content"""
        return Task(
            config=self.tasks_config['refine_readme_task']
        )
    
    @task
    def create_pr_task(self) -> Task:
        """Task for creating pull requests"""
        return Task(
            config=self.tasks_config['create_pr_task']
        )
    


    @crew
    def crew(self) -> Crew:
        """Create the README SEO Booster crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
