
import React from "react";
import Form from "@rjsf/bootstrap-4";

const schema = {
  title: "Exchange Credential",
  type: "object",
  properties: {
    label: { type: "string", title: "Label" },
    is_service: { type: "boolean", title: "Is Service", default: true },
    is_active: { type: "boolean", title: "Active", default: true },

    api_key: { type: "string", title: "API Key" },
    api_secret: { type: "string", title: "API Secret" },
    api_passphrase: { type: "string", title: "API Passphrase" },
    subaccount: { type: "string", title: "Subaccount" },

    scopes: { type: "array", title: "Scopes", items: { type: "string" } },

    secret_ref: { type: "string", title: "Secret Ref" },
    vault_path: { type: "string", title: "Vault Path" },

    valid_from: { type: "string", format: "date-time", title: "Valid From" },
    valid_to: { type: "string", format: "date-time", title: "Valid To" },

    created_at: { type: "string", format: "date-time", title: "Created At" }
  }
};

const uiSchema = {
  api_secret: { "ui:widget": "password" },
  is_service: { "ui:widget": "checkbox" },
  is_active: { "ui:widget": "checkbox" },
  scopes: { "ui:widget": "textarea" },
  created_at: { "ui:disabled": true },
};

export default function ExchangeCredentialForm({ formData, onSubmit }) {
  return (
    <Form
      schema={schema}
      uiSchema={uiSchema}
      formData={formData}
      onSubmit={({ formData }) => onSubmit(formData)}
    />
  );
}
