import React from "react";
import Form from "@rjsf/bootstrap-4";

const schema = {
  title: "Exchange Status History",
  type: "array",
  items: {
    type: "object",
    properties: {
      event: { type: "string", title: "Event" },          // e.g. symbols_refresh
      status: { type: "string", title: "Status" },        // ok / error
      message: { type: "string", title: "Message" },      // optional text
      created_at: { type: "string", format: "date-time", title: "Created At" }
    }
  }
};

const uiSchema = {
  "ui:readonly": true
};

export default function ExchangeHistoryForm({ formData }) {
  return <Form schema={schema} uiSchema={uiSchema} formData={formData} />;
}
