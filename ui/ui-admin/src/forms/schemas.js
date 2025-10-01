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

    fetch_symbols_interval_min: {
      type: "integer",
      title: "Fetch Symbols Interval (min)",
      default: 60,
    },
    fetch_filters_interval_min: {
      type: "integer",
      title: "Fetch Filters Interval (min)",
      default: 1440,
    },
    fetch_limits_interval_min: {
      type: "integer",
      title: "Fetch Limits Interval (min)",
      default: 1440,
    },

    rate_limit_per_min: {
      type: "integer",
      title: "Rate Limit (per min)",
    },
    recv_window_ms: {
      type: "integer",
      title: "Recv Window (ms)",
      default: 5000,
    },
    request_timeout_ms: {
      type: "integer",
      title: "Request Timeout (ms)",
      default: 10000,
    },

    is_active: {
      type: "boolean",
      title: "Active",
      default: true,
    },

    features: {
      type: "object",
      title: "Features (JSON)",
      additionalProperties: true,
      default: {},
    },
    extra: {
      type: "object",
      title: "Extra (JSON)",
      additionalProperties: true,
      default: {},
    },
  },
  required: ["code", "name", "kind", "environment"],
};
export const ExchangeCredentialFormSchema = {
  title: "Exchange Credential",
  type: "object",
  properties: {
    label: { type: "string", title: "Label" },

    is_service: {
      type: "boolean",
      title: "Service Credential",
      default: true,
    },
    is_active: {
      type: "boolean",
      title: "Active",
      default: true,
    },

    api_key: { type: "string", title: "API Key" },
    api_secret: { type: "string", title: "API Secret" },
    api_passphrase: { type: "string", title: "API Passphrase" },

    subaccount: { type: "string", title: "Subaccount" },

//    scopes: {
//      type: "array",
//      title: "Scopes",
//      items: { type: "string" },
//      default: [],
//    },

    secret_ref: { type: "string", title: "Secret Ref" },
    vault_path: { type: "string", title: "Vault Path" },

//    valid_from: { type: "string", format: "date-time", title: "Valid From" },
//    valid_to: { type: "string", format: "date-time", title: "Valid To" },
  },
  required: ["api_key", "api_secret"],
};
