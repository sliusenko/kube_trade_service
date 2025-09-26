import React from "react";
import Form from "@rjsf/bootstrap-4";

const schema = {
  title: "Exchange",
  type: "object",
  required: ["code", "name"],
  properties: {
    code: { type: "string", title: "Code" },
    name: { type: "string", title: "Name" },
    kind: { type: "string", title: "Kind", enum: ["spot", "futures", "margin"] },
    environment: { type: "string", title: "Environment", enum: ["prod", "dev", "test"] },
    base_url_public: { type: "string", title: "Base URL Public" },
    base_url_private: { type: "string", title: "Base URL Private" },
    is_active: { type: "boolean", title: "Active" }
  },
};

export default function ExchangeForm({ formData, onChange, onSubmit }) {
  return (
    <Form
      schema={schema}
      formData={formData}
      onChange={onChange}
      onSubmit={onSubmit}
    />
  );
}
