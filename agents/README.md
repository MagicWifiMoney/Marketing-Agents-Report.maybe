# Marketing Agency Sub Agents

This directory contains 3 specialized sub agents designed to work together for comprehensive marketing agency workflows.

## Quick Start

### 1. Agent Overview
- **Content Creator Agent**: Specializes in content creation, copywriting, and SEO optimization
- **Design & Creative Agent**: Focuses on visual design, branding, and creative direction
- **Strategy & Analytics Agent**: Handles marketing strategy, data analysis, and campaign optimization

### 2. Directory Structure
```
agents/
├── content-creator/
│   ├── config/agent.yaml
│   ├── prompts/system_prompt.txt
│   └── templates/blog_post_template.md
├── design-creative/
│   ├── config/agent.yaml
│   ├── prompts/system_prompt.txt
│   └── templates/brand_guidelines_template.md
├── strategy-analytics/
│   ├── config/agent.yaml
│   ├── prompts/system_prompt.txt
│   └── templates/campaign_strategy_template.md
├── workflows/
│   ├── README.md
│   ├── content-creation-workflow.md
│   ├── campaign-development-workflow.md
│   └── brand-development-workflow.md
└── sub-agents-setup.md
```

### 3. Copy/Paste Instructions

#### For Content Creator Agent:
1. Copy the system prompt from `content-creator/prompts/system_prompt.txt`
2. Use the blog post template from `content-creator/templates/blog_post_template.md`
3. Configure using `content-creator/config/agent.yaml`

#### For Design & Creative Agent:
1. Copy the system prompt from `design-creative/prompts/system_prompt.txt`
2. Use the brand guidelines template from `design-creative/templates/brand_guidelines_template.md`
3. Configure using `design-creative/config/agent.yaml`

#### For Strategy & Analytics Agent:
1. Copy the system prompt from `strategy-analytics/prompts/system_prompt.txt`
2. Use the campaign strategy template from `strategy-analytics/templates/campaign_strategy_template.md`
3. Configure using `strategy-analytics/config/agent.yaml`

### 4. Agent Collaboration Workflows

#### Content Creation Workflow:
- **Duration:** 6-10 days
- **Process:** Strategy → Content → Design → Optimization
- **Best For:** Blog posts, social media content, email campaigns
- **Details:** See `workflows/content-creation-workflow.md`

#### Campaign Development Workflow:
- **Duration:** 2-8 weeks
- **Process:** Strategy → Creative → Setup → Execution → Analysis
- **Best For:** Multi-channel campaigns, product launches
- **Details:** See `workflows/campaign-development-workflow.md`

#### Brand Development Workflow:
- **Duration:** 6-12 weeks
- **Process:** Strategy → Visual Identity → Brand Voice → Implementation
- **Best For:** New brands, brand refreshes, comprehensive identity
- **Details:** See `workflows/brand-development-workflow.md`

### 5. Usage Examples

#### Creating a Blog Post:
```bash
# 1. Use Strategy Agent to define target audience and objectives
# 2. Use Content Agent to create blog content
# 3. Use Design Agent to create featured images
# 4. Use Strategy Agent to set up tracking and optimization
```

#### Developing Brand Guidelines:
```bash
# 1. Use Strategy Agent to analyze brand positioning
# 2. Use Design Agent to create visual identity system
# 3. Use Content Agent to write brand voice guidelines
# 4. Use Strategy Agent to validate brand strategy
```

### 6. Templates & Workflows Available

#### Content Creator Templates:
- Blog post template
- Social media content template
- Email campaign template

#### Design Creative Templates:
- Brand guidelines template
- Logo usage guide template
- Design system template

#### Strategy Analytics Templates:
- Campaign strategy template
- Performance report template
- Market analysis template

#### Workflow Templates:
- Content Creation Workflow (6-10 days)
- Campaign Development Workflow (2-8 weeks)
- Brand Development Workflow (6-12 weeks)

### 7. Best Practices

#### Agent Communication:
- Always start with Strategy Agent for objectives
- Use Content Agent for messaging and copy
- Use Design Agent for visual elements
- Return to Strategy Agent for optimization

#### Template Usage:
- Customize templates for each project
- Maintain consistency across all agents
- Update templates based on performance data
- Share learnings between agents

#### Performance Tracking:
- Set clear KPIs for each agent
- Track collaboration efficiency
- Monitor output quality
- Optimize workflows based on results

### 8. Troubleshooting

#### Common Issues:
- **Agent conflicts**: Ensure clear role definitions
- **Template confusion**: Use consistent naming conventions
- **Workflow bottlenecks**: Establish clear handoff points
- **Quality issues**: Implement review processes

#### Solutions:
- Review agent configurations
- Update system prompts as needed
- Refine collaboration workflows
- Implement quality assurance processes

---

## Support

For questions or issues with the sub agents:
1. Check the configuration files
2. Review the system prompts
3. Consult the templates
4. Refer to the main setup document: `sub-agents-setup.md`

---

*Last Updated: [Current Date]*
*Version: 1.0*
