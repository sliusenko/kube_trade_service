import React from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";

const schema = {
  title: "Exchange",
  type: "object",
  properties: {
    code: { type: "string", title: "Code" },
    name: { type: "string", title: "Name" },
    kind: {
      type: "string",
      title: "Kind",
      enum: ["spot", "futures", "margin"]
    },
    environment: {
      type: "string",
      title: "Environment",
      enum: ["prod", "dev", "test"]
    },
    base_url_public: { type: "string", title: "Base URL Public" },
    base_url_private: { type: "string", title: "Base URL Private" },
    ws_public_url: { type: "string", title: "WS Public URL" },
    ws_private_url: { type: "string", title: "WS Private URL" },
    data_feed_url: { type: "string", title: "Data Feed URL" },
    features: { type: "object", title: "Features" },
    extra: { type: "object", title: "Extra" },
    is_active: { type: "boolean", title: "Active" }
  }
};

const uiSchema = {
  features: { "ui:widget": "textarea" },
  extra: { "ui:widget": "textarea" },
  is_active: { "ui:widget": "checkbox" }
};

export default function ExchangeForm({ formData, onSubmit }) {
  return (
    <Form
      schema={schema}
      uiSchema={uiSchema}
      validator={validator}
      formData={formData}
      onSubmit={({ formData }) => onSubmit(formData)}
    />
  );
}
