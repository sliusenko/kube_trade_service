import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControlLabel,
  Checkbox,
} from "@mui/material";

const ExchangeForm = ({ open, onClose, onSave, initialData }) => {
  const [form, setForm] = useState({
    name: "",
    type: "",
    api_url: "",
    refresh_interval: 60,
    is_active: true,
  });

  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    } else {
      setForm({
        name: "",
        type: "",
        api_url: "",
        refresh_interval: 60,
        is_active: true,
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckbox = (e) => {
    setForm((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleSubmit = () => {
    onSave(form);
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{initialData ? "Edit Exchange" : "Add Exchange"}</DialogTitle>
      <DialogContent sx={{ display: "grid", gap: 2, width: 400 }}>
        <TextField
          label="Name"
          name="name"
          value={form.name}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Type"
          name="type"
          value={form.type}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="API URL"
          name="api_url"
          value={form.api_url}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Refresh Interval (s)"
          name="refresh_interval"
          type="number"
          value={form.refresh_interval}
          onChange={handleChange}
          fullWidth
        />
        <FormControlLabel
          control={<Checkbox checked={form.is_active} onChange={handleCheckbox} />}
          label="Active"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSubmit}>
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ExchangeForm;
