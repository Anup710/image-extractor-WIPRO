import React from 'react';

interface Template {
  id: string;
  name: string;
  description: string;
}

interface TemplateSelectorProps {
  selectedTemplate: string;
  onTemplateChange: (template: string) => void;
}

const templates: Template[] = [
  {
    id: 'default',
    name: 'Default Analysis',
    description: 'General analysis without specific focus'
  },
  {
    id: 'analyze',
    name: 'Detailed Analysis',
    description: 'Comprehensive insights and detailed examination'
  },
  {
    id: 'describe',
    name: 'Description Mode',
    description: 'Focus on describing what is visible in the images'
  },
  {
    id: 'technical',
    name: 'Technical Analysis',
    description: 'Technical aspects and professional evaluation'
  }
];

const TemplateSelector: React.FC<TemplateSelectorProps> = ({
  selectedTemplate,
  onTemplateChange
}) => {
  return (
    <div className="template-selector">
      <h3>Analysis Mode</h3>
      <p className="template-description">
        Choose how you want the AI to analyze your images:
      </p>

      <div className="template-options">
        {templates.map((template) => (
          <label key={template.id} className="template-option">
            <input
              type="radio"
              name="template"
              value={template.id}
              checked={selectedTemplate === template.id}
              onChange={(e) => onTemplateChange(e.target.value)}
            />
            <div className="template-content">
              <h4>{template.name}</h4>
              <p>{template.description}</p>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};

export default TemplateSelector;