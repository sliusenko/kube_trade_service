import React from "react";
import Form from "@rjsf/bootstrap-4";

const schema = {
  title: "Exchange Limits",
  type: "array",
  items: {
    type: "object",
    properties: {
      limit_type: { type: "string", title: "Limit Type" },
      interval_unit: { type: "string", title: "Interval Unit" },
      interval_num: { type: "integer", title: "Interval Num" },
      limit: { type: "integer", title: "Limit" },
      fetched_at: { type: "string", format: "date-time", title: "Fetched At" }
    }
  }
};

const uiSchema = {
  "ui:readonly": true
};

export default function ExchangeLimitForm({ formData }) {
  return <Form schema={schema} uiSchema={uiSchema} formData={formData} />;
}
