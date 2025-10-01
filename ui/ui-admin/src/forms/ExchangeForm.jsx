import React from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";

export default function ExchangeForm({ formData, onSubmit }) {
  const [schema, setSchema] = useState(null);

  useEffect(() => {
    fetch("/api/exchanges/schema")
      .then((res) => res.json())
      .then(setSchema)
      .catch(console.error);
  }, []);

  if (!schema) return <p>Loading schema...</p>;

  return (
    <Form
      schema={schema}
      validator={validator}
      formData={formData}
      onSubmit={({ formData }) => onSubmit(formData)}
    />
  );
}
