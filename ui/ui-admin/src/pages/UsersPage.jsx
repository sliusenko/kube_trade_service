import { useState, useEffect } from "react";
import {
  Tabs,
  Tab,
  Box,
  Button,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { Add, Edit, Delete } from "@mui/icons-material";

// API
import { getUsers, createUser, updateUser, deleteUser } from "../api/users";
import { getRoles, createRole, updateRole, deleteRole } from "../api/roles";
import { getPermissions, createPermission, updatePermission, deletePermission } from "../api/permissions";
import { getRolePermissions, createRolePermission, deleteRolePermission } from "../api/role_permissions";

export default function AdminPage() {
  const [tab, setTab] = useState(0);

  // === USERS ===
  const [users, setUsers] = useState([]);
  const [userForm, setUserForm] = useState({ username: "", email: "", role: "user", password: "", is_active: true });
  const [openUser, setOpenUser] = useState(false);
  const [editUser, setEditUser] = useState(null);

  // Password validation state
  const [passwordError, setPasswordError] = useState("");

  const loadUsers = () => getUsers().then(setUsers);
  useEffect(() => { loadUsers(); }, []);

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setUserForm({ ...userForm, password: value });

    if (!editUser && value.length > 0 && value.length < 8) {
      setPasswordError("Password must be at least 8 characters long");
    } else {
      setPasswordError("");
    }
  };

  const handleSaveUser = async () => {
    try {
      if (!editUser && userForm.password.length < 8) {
        alert("Password must be at least 8 characters long");
        return;
      }

      if (editUser) {
        const payload = {
          email: userForm.email,
          role: userForm.role,
          is_active: userForm.is_active
        };
        if (userForm.password) {
          payload.password = userForm.password;
        }
        await updateUser(editUser.user_id, payload);
      } else {
        await createUser(userForm);
      }
      loadUsers();
      setOpenUser(false);
    } catch (err) {
      console.error(err);
      const msg = err?.response?.data?.detail || err.message || "Помилка при збереженні користувача";
      alert(msg);
    }
  };

  // === ROLES ===
  const [roles, setRoles] = useState([]);
  const [roleForm, setRoleForm] = useState({ name: "", description: "" });
  const [openRole, setOpenRole] = useState(false);
  const [editRole, setEditRole] = useState(null);

  const loadRoles = () => getRoles().then(setRoles);
  useEffect(() => { loadRoles(); }, []);

  const handleSaveRole = async () => {
    try {
      if (editRole) {
        await updateRole(editRole.name, roleForm);
      } else {
        await createRole(roleForm);
      }
      loadRoles();
      setOpenRole(false);
    } catch (err) {
      console.error(err);
      alert("Помилка при збереженні ролі");
    }
  };

  // === PERMISSIONS ===
  const [permissions, setPermissions] = useState([]);
  const [permForm, setPermForm] = useState({ name: "", description: "" });
  const [openPerm, setOpenPerm] = useState(false);
  const [editPerm, setEditPerm] = useState(null);

  const loadPermissions = () => getPermissions().then(setPermissions);
  useEffect(() => { loadPermissions(); }, []);

  const handleSavePerm = async () => {
    try {
      if (editPerm) {
        await updatePermission(editPerm.name, permForm);
      } else {
        await createPermission(permForm);
      }
      loadPermissions();
      setOpenPerm(false);
    } catch (err) {
      console.error(err);
      alert("Помилка при збереженні permission");
    }
  };

  // === ROLE PERMISSIONS ===
  const [rolePerms, setRolePerms] = useState([]);
  const [rpForm, setRpForm] = useState({ role_name: "", permission_name: "" });
  const [openRp, setOpenRp] = useState(false);

  const loadRolePerms = () => getRolePermissions().then(setRolePerms);
  useEffect(() => { loadRolePerms(); }, []);

  const handleSaveRp = async () => {
    try {
      await createRolePermission(rpForm);
      loadRolePerms();
      setOpenRp(false);
    } catch (err) {
      console.error(err);
      alert("Помилка при створенні role-permission (можливо вже існує)");
    }
  };

  // === RENDER ===
  return (
    <Box sx={{ p: 2 }}>
      <Tabs value={tab} onChange={(e, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Users" />
        <Tab label="Roles" />
        <Tab label="Permissions" />
        <Tab label="Role Permissions" />
      </Tabs>

      {/* USERS */}
      {tab === 0 && (
        <>
          <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
            <Button startIcon={<Add />} onClick={() => {
              setEditUser(null);
              setUserForm({ username: "", email: "", role: "user", password: "", is_active: true });
              setPasswordError("");
              setOpenUser(true);
            }}>
              Add User
            </Button>
          </Stack>
          <DataGrid rows={users} getRowId={(r) => r.user_id}
            columns={[
              { field: "username", headerName: "Username", flex: 1 },
              { field: "email", headerName: "Email", flex: 1 },
              { field: "role", headerName: "Role", width: 120 },
              {
                field: "is_active", headerName: "Active", width: 100,
                renderCell: (p) => (p.value ? "✅" : "❌")
              },
              {
                field: "actions", headerName: "Actions", width: 180,
                renderCell: (p) => (
                  <Stack direction="row" spacing={1}>
                    <Button startIcon={<Edit />} onClick={() => {
                      setEditUser(p.row);
                      setUserForm({ ...p.row, password: "" });
                      setPasswordError("");
                      setOpenUser(true);
                    }}>Edit</Button>
                    <Button color="error" startIcon={<Delete />} onClick={async () => {
                      try {
                        await deleteUser(p.row.user_id);
                        loadUsers();
                      } catch (err) {
                        console.error(err);
                        alert("Помилка при видаленні користувача");
                      }
                    }}>Delete</Button>
                  </Stack>
                )
              }
            ]}
            autoHeight
          />
          <Dialog open={openUser} onClose={() => setOpenUser(false)}>
            <DialogTitle>{editUser ? "Edit User" : "Add User"}</DialogTitle>
            <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
              <TextField
                label="Username"
                value={userForm.username}
                onChange={e => setUserForm({ ...userForm, username: e.target.value })}
                disabled={!!editUser}
              />
              <TextField
                label="Email"
                value={userForm.email}
                onChange={e => setUserForm({ ...userForm, email: e.target.value })}
              />
              <TextField
                label={editUser ? "Password (leave blank to keep unchanged)" : "Password"}
                type="password"
                value={userForm.password}
                onChange={handlePasswordChange}
                error={!!passwordError}
                helperText={passwordError}
              />
              <Select
                value={userForm.role}
                onChange={e => setUserForm({ ...userForm, role: e.target.value })}
              >
                {roles.map((r) => (
                  <MenuItem key={r.name} value={r.name}>{r.name}</MenuItem>
                ))}
              </Select>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenUser(false)}>Cancel</Button>
              <Button
                onClick={handleSaveUser}
                disabled={!editUser && (userForm.password.length < 8 || !!passwordError)}
              >
                Save
              </Button>
            </DialogActions>
          </Dialog>
        </>
      )}

      {/* ROLES */}
      {tab === 1 && (
        <>
          <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
            <Button startIcon={<Add />} onClick={() => { setEditRole(null); setRoleForm({ name: "", description: "" }); setOpenRole(true); }}>
              Add Role
            </Button>
          </Stack>
          <DataGrid rows={roles} getRowId={(r) => r.name}
            columns={[
              { field: "name", headerName: "Name", flex: 1 },
              { field: "description", headerName: "Description", flex: 1 },
              {
                field: "actions", headerName: "Actions", width: 180,
                renderCell: (p) => (
                  <Stack direction="row" spacing={1}>
                    <Button startIcon={<Edit />} onClick={() => { setEditRole(p.row); setRoleForm(p.row); setOpenRole(true); }}>Edit</Button>
                    <Button color="error" startIcon={<Delete />} onClick={async () => {
                      try {
                        await deleteRole(p.row.name);
                        loadRoles();
                      } catch (err) {
                        console.error(err);
                        alert("Помилка при видаленні ролі");
                      }
                    }}>Delete</Button>
                  </Stack>
                )
              }
            ]}
            autoHeight
          />
          <Dialog open={openRole} onClose={() => setOpenRole(false)}>
            <DialogTitle>{editRole ? "Edit Role" : "Add Role"}</DialogTitle>
            <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
              <TextField label="Name" value={roleForm.name} onChange={e => setRoleForm({ ...roleForm, name: e.target.value })} disabled={!!editRole} />
              <TextField label="Description" value={roleForm.description} onChange={e => setRoleForm({ ...roleForm, description: e.target.value })} />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenRole(false)}>Cancel</Button>
              <Button onClick={handleSaveRole}>Save</Button>
            </DialogActions>
          </Dialog>
        </>
      )}

      {/* PERMISSIONS */}
      {tab === 2 && (
        <>
          <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
            <Button startIcon={<Add />} onClick={() => { setEditPerm(null); setPermForm({ name: "", description: "" }); setOpenPerm(true); }}>
              Add Permission
            </Button>
          </Stack>
          <DataGrid rows={permissions} getRowId={(r) => r.name}
            columns={[
              { field: "name", headerName: "Name", flex: 1 },
              { field: "description", headerName: "Description", flex: 1 },
              {
                field: "actions", headerName: "Actions", width: 180,
                renderCell: (p) => (
                  <Stack direction="row" spacing={1}>
                    <Button startIcon={<Edit />} onClick={() => { setEditPerm(p.row); setPermForm(p.row); setOpenPerm(true); }}>Edit</Button>
                    <Button color="error" startIcon={<Delete />} onClick={async () => {
                      try {
                        await deletePermission(p.row.name);
                        loadPermissions();
                      } catch (err) {
                        console.error(err);
                        alert("Помилка при видаленні permission");
                      }
                    }}>Delete</Button>
                  </Stack>
                )
              }
            ]}
            autoHeight
          />
          <Dialog open={openPerm} onClose={() => setOpenPerm(false)}>
            <DialogTitle>{editPerm ? "Edit Permission" : "Add Permission"}</DialogTitle>
            <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
              <TextField label="Name" value={permForm.name} onChange={e => setPermForm({ ...permForm, name: e.target.value })} disabled={!!editPerm} />
              <TextField label="Description" value={permForm.description} onChange={e => setPermForm({ ...permForm, description: e.target.value })} />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenPerm(false)}>Cancel</Button>
              <Button onClick={handleSavePerm}>Save</Button>
            </DialogActions>
          </Dialog>
        </>
      )}

      {/* ROLE PERMISSIONS */}
      {tab === 3 && (
        <>
          <Stack direction="row" justifyContent="flex-end" sx={{ mb: 2 }}>
            <Button startIcon={<Add />} onClick={() => { setRpForm({ role_name: "", permission_name: "" }); setOpenRp(true); }}>
              Add Role Permission
            </Button>
          </Stack>
          <DataGrid rows={rolePerms} getRowId={(r) => `${r.role_name}-${r.permission_name}`}
            columns={[
              { field: "role_name", headerName: "Role", flex: 1 },
              { field: "permission_name", headerName: "Permission", flex: 1 },
              {
                field: "actions", headerName: "Actions", width: 180,
                renderCell: (p) => (
                  <Stack direction="row" spacing={1}>
                    <Button color="error" startIcon={<Delete />} onClick={async () => {
                      try {
                        await deleteRolePermission(p.row.role_name, p.row.permission_name);
                        loadRolePerms();
                      } catch (err) {
                        console.error(err);
                        alert("Помилка при видаленні role-permission");
                      }
                    }}>Delete</Button>
                  </Stack>
                )
              }
            ]}
            autoHeight
          />
          <Dialog open={openRp} onClose={() => setOpenRp(false)}>
            <DialogTitle>Add Role Permission</DialogTitle>
            <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
              <Select value={rpForm.role_name} onChange={(e) => setRpForm({ ...rpForm, role_name: e.target.value })}>
                {roles.map((r) => (
                  <MenuItem key={r.name} value={r.name}>{r.name}</MenuItem>
                ))}
              </Select>
              <Select value={rpForm.permission_name} onChange={(e) => setRpForm({ ...rpForm, permission_name: e.target.value })}>
                {permissions.map((p) => (
                  <MenuItem key={p.name} value={p.name}>{p.name}</MenuItem>
                ))}
              </Select>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenRp(false)}>Cancel</Button>
              <Button onClick={handleSaveRp} disabled={!rpForm.role_name || !rpForm.permission_name}>Save</Button>
            </DialogActions>
          </Dialog>
        </>
      )}
    </Box>
  );
}
