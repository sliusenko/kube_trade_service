import { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import {
  Button,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControlLabel,
  Checkbox
} from "@mui/material";
import { Add, Edit, Delete } from "@mui/icons-material";
import { getUsers, createUser, updateUser, deleteUser } from "../api/users";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [open, setOpen] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "user",
    is_active: true
  });

  const loadUsers = () => {
    getUsers()
      .then(setUsers)
      .catch((err) => console.error("Error fetching users:", err));
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleOpen = (user = null) => {
    if (user) {
      setEditUser(user);
      setForm({
        username: user.username,
        email: user.email,
        password: "",
        role: user.role || "user",
        is_active: user.is_active ?? true
      });
    } else {
      setEditUser(null);
      setForm({
        username: "",
        email: "",
        password: "",
        role: "user",
        is_active: true
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = async () => {
    try {
      if (editUser) {
        await updateUser(editUser.user_id, {
          email: form.email,
          role: form.role,
          is_active: form.is_active
        });
      } else {
        await createUser({
          username: form.username,
          email: form.email,
          password: form.password,
          role: form.role,
          is_active: form.is_active
        });
      }
      loadUsers();
      handleClose();
    } catch (err) {
      console.error("Error saving user:", err);
    }
  };

  const handleDelete = async (row) => {
    if (!window.confirm(`Delete user ${row.username}?`)) return;
    try {
      await deleteUser(row.user_id);
      loadUsers();
    } catch (err) {
      console.error("Error deleting user:", err);
    }
  };

  const columns = [
    { field: "user_id", headerName: "User ID", width: 150 },
    { field: "username", headerName: "Username", flex: 1 },
    { field: "email", headerName: "Email", flex: 1.5 },
    { field: "role", headerName: "Role", width: 120 },
    { field: "is_active", headerName: "Active", width: 100 },
    {
      field: "actions",
      headerName: "Actions",
      width: 180,
      sortable: false,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <Button
            size="small"
            variant="outlined"
            color="primary"
            startIcon={<Edit />}
            onClick={() => handleOpen(params.row)}
          >
            Edit
          </Button>
          <Button
            size="small"
            variant="outlined"
            color="error"
            startIcon={<Delete />}
            onClick={() => handleDelete(params.row)}
          >
            Delete
          </Button>
        </Stack>
      )
    }
  ];

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ marginBottom: 16 }}>Users</h1>

      <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add User
        </Button>
      </Stack>

      <div style={{ height: 500, width: "100%" }}>
        <DataGrid
          rows={users}
          getRowId={(row) => row.user_id}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[5, 10, 20]}
        />
      </div>

      {/* Dialog */}
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{editUser ? "Edit User" : "Add User"}</DialogTitle>
        <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
          {!editUser && (
            <TextField
              label="Username"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              fullWidth
            />
          )}
          <TextField
            label="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            fullWidth
          />
          {!editUser && (
            <TextField
              label="Password"
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              fullWidth
            />
          )}
          <TextField
            select
            label="Role"
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
            fullWidth
          >
            <MenuItem value="admin">Admin</MenuItem>
            <MenuItem value="user">User</MenuItem>
          </TextField>
          <FormControlLabel
            control={
              <Checkbox
                checked={form.is_active}
                onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
              />
            }
            label="Active"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {editUser ? "Save" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
