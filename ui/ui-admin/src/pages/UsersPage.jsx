import { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Button, Stack } from "@mui/material";
import { Add, Edit, Delete } from "@mui/icons-material";
import { getUsers, createUser, updateUser, deleteUser } from "../api/users";

export default function UsersPage() {
  const [users, setUsers] = useState([]);

  const loadUsers = () => {
    getUsers()
      .then(setUsers)
      .catch((err) => console.error("Error fetching users:", err));
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleAdd = async () => {
    const username = prompt("Enter username:");
    const email = prompt("Enter email:");
    const password = prompt("Enter password:");
    if (!username || !email || !password) return;

    try {
      await createUser({
        username,
        email,
        password_hash: password, // бекенд очікує password_hash
        role: "user", // дефолт
      });
      loadUsers();
    } catch (err) {
      console.error("Error creating user:", err);
    }
  };

  const handleEdit = async (row) => {
    const newEmail = prompt("Enter new email:", row.email);
    if (!newEmail) return;

    try {
      await updateUser(row.user_id, { ...row, email: newEmail });
      loadUsers();
    } catch (err) {
      console.error("Error updating user:", err);
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
            onClick={() => handleEdit(params.row)}
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
      ),
    },
  ];

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ marginBottom: 16 }}>Users</h1>

      <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={handleAdd}
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
    </div>
  );
}
