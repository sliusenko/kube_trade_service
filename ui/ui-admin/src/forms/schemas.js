// JSON Schema для форм (локальні, без бекенду)

export const ExchangeFormSchema = {
  title: "Exchange",
  type: "object",
  properties: {
    code: { type: "string", title: "Code" },
    name: { type: "string", title: "Name" },
    kind: {
      type: "string",
      title: "Kind",
      enum: ["spot", "futures", "margin"],
      default: "spot",
    },
    environment: {
      type: "string",
      title: "Environment",
      enum: ["prod", "dev", "test"],
      default: "prod",
    },
    base_url_public: { type: "string", title: "Base URL Public" },
    base_url_private: { type: "string", title: "Base URL Private" },
    ws_public_url: { type: "string", title: "WS Public URL" },
    ws_private_url: { type: "string", title: "WS Private URL" },
    data_feed_url: { type: "string", title: "Data Feed URL" },
    is_active: { type: "boolean", title: "Active", default: true },
  },
  required: ["code", "name", "kind", "environment"],
};

export const ExchangeCredentialFormSchema = {
  title: "Exchange Credential",
  type: "object",
  properties: {
    label: { type: "string", title: "Label" },
    api_key: { type: "string", title: "API Key" },
    api_secret: { type: "string", title: "API Secret" },
    api_passphrase: { type: "string", title: "API Passphrase" },
    subaccount: { type: "string", title: "Subaccount" },
    is_service: { type: "boolean", title: "Service Account?", default: true },
    is_active: { type: "boolean", title: "Active", default: true },
  },
  required: ["api_key", "api_secret"],
};
