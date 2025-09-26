import React from "react";
import Form from "@rjsf/bootstrap-4";

const schema = {
  title: "Exchange Symbols",
  type: "array",
  items: {
    type: "object",
    properties: {
      symbol: { type: "string", title: "Symbol" },
      base_asset: { type: "string", title: "Base Asset" },
      quote_asset: { type: "string", title: "Quote Asset" },
      status: { type: "string", title: "Status" },
      type: { type: "string", title: "Type" },
      step_size: { type: "number", title: "Step Size" },
      tick_size: { type: "number", title: "Tick Size" },
      min_qty: { type: "number", title: "Min Qty" },
      max_qty: { type: "number", title: "Max Qty" },
      min_notional: { type: "number", title: "Min Notional" },
      max_notional: { type: "number", title: "Max Notional" },
      is_active: { type: "boolean", title: "Active" },
      fetched_at: { type: "string", format: "date-time", title: "Fetched At" }
    }
  }
};

const uiSchema = {
  "ui:readonly": true
};

export default function ExchangeSymbolForm({ formData }) {
  return <Form schema={schema} uiSchema={uiSchema} formData={formData} />;
}
