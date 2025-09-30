import React, { useEffect, useState } from "react";
import {
  Tabs,
  Tab,
  Box,
  Paper,
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TextField,
} from "@mui/material";
import { Add, Delete } from "@mui/icons-material";

import {
  getTimeframes,
  createTimeframe,
  deleteTimeframe,
  getCommands,
  createCommand,
  deleteCommand,
  getReasons,
  createReason,
  deleteReason,
  getTradeProfiles,
  createTradeProfile,
  deleteTradeProfile,
  getTradeConditions,
  createTradeCondition,
  deleteTradeCondition,
  getGroupIcons,
  createGroupIcon,
  deleteGroupIcon,
} from "../api/config";

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
}

export default function PageConfig() {
  const [tab, setTab] = useState(0);

  // ---- Timeframes ----
  const [timeframes, setTimeframes] = useState([]);
  const [tfForm, setTfForm] = useState({ code: "", history_limit: "", min_len: "", hours: "", lookback: "" });

  async function loadTimeframes() { setTimeframes(await getTimeframes()); }
  async function addTimeframe(e) {
    e.preventDefault();
    await createTimeframe(tfForm);
    setTfForm({ code: "", history_limit: "", min_len: "", hours: "", lookback: "" });
    loadTimeframes();
  }
  async function removeTimeframe(code) {
    if (window.confirm("Видалити таймфрейм?")) {
      await deleteTimeframe(code); loadTimeframes();
    }
  }

  // ---- Commands ----
  const [commands, setCommands] = useState([]);
  const [cmdForm, setCmdForm] = useState({ command: "", group_name: "", description: "" });

  async function loadCommands() { setCommands(await getCommands()); }
  async function addCommand(e) {
    e.preventDefault();
    await createCommand(cmdForm);
    setCmdForm({ command: "", group_name: "", description: "" });
    loadCommands();
  }
  async function removeCommand(id) {
    if (window.confirm("Видалити команду?")) {
      await deleteCommand(id); loadCommands();
    }
  }

  // ---- Reasons ----
  const [reasons, setReasons] = useState([]);
  const [reasonForm, setReasonForm] = useState({ code: "", description: "", category: "" });

  async function loadReasons() { setReasons(await getReasons()); }
  async function addReason(e) {
    e.preventDefault();
    await createReason(reasonForm);
    setReasonForm({ code: "", description: "", category: "" });
    loadReasons();
  }
  async function removeReason(code) {
    if (window.confirm("Видалити reason?")) {
      await deleteReason(code); loadReasons();
    }
  }

  // ---- Trade Profiles ----
  const [profiles, setProfiles] = useState([]);
  const [profileForm, setProfileForm] = useState({ name: "", description: "" });

  async function loadProfiles() { setProfiles(await getTradeProfiles()); }
  async function addProfile(e) {
    e.preventDefault();
    await createTradeProfile(profileForm);
    setProfileForm({ name: "", description: "" });
    loadProfiles();
  }
  async function removeProfile(id) {
    if (window.confirm("Видалити профіль?")) {
      await deleteTradeProfile(id); loadProfiles();
    }
  }

  // ---- Trade Conditions ----
  const [conditions, setConditions] = useState([]);
  const [conditionForm, setConditionForm] = useState({
    profile_id: "",
    action: "",
    condition_type: "",
    param_1: "",
    param_2: "",
    priority: "",
  });

  async function loadConditions() { setConditions(await getTradeConditions()); }
  async function addCondition(e) {
    e.preventDefault();
    await createTradeCondition(conditionForm);
    setConditionForm({ profile_id: "", action: "", condition_type: "", param_1: "", param_2: "", priority: "" });
    loadConditions();
  }
  async function removeCondition(id) {
    if (window.confirm("Видалити condition?")) {
      await deleteTradeCondition(id); loadConditions();
    }
  }

  // ---- Group Icons ----
  const [icons, setIcons] = useState([]);
  const [iconForm, setIconForm] = useState({ group_name: "", icon: "" });

  async function loadIcons() { setIcons(await getGroupIcons()); }
  async function addIcon(e) {
    e.preventDefault();
    await createGroupIcon(iconForm);
    setIconForm({ group_name: "", icon: "" });
    loadIcons();
  }
  async function removeIcon(name) {
    if (window.confirm("Видалити іконку?")) {
      await deleteGroupIcon(name); loadIcons();
    }
  }

  // ---- Lifecycle ----
  useEffect(() => {
    loadTimeframes();
    loadCommands();
    loadReasons();
    loadProfiles();
    loadConditions();
    loadIcons();
  }, []);

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Core Config</h1>

      <Paper>
        <Tabs value={tab} onChange={(e, v) => setTab(v)} indicatorColor="primary" textColor="primary">
          <Tab label="Timeframes" />
          <Tab label="Commands" />
          <Tab label="Reasons" />
          <Tab label="Trade Profiles" />
          <Tab label="Trade Conditions" />
          <Tab label="Group Icons" />
        </Tabs>
      </Paper>

      {/* ---- Timeframes ---- */}
      <TabPanel value={tab} index={0}>
        <form onSubmit={addTimeframe} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Code" value={tfForm.code} onChange={(e) => setTfForm({ ...tfForm, code: e.target.value })} />
          <TextField label="History Limit" value={tfForm.history_limit} onChange={(e) => setTfForm({ ...tfForm, history_limit: e.target.value })} />
          <TextField label="Min Len" value={tfForm.min_len} onChange={(e) => setTfForm({ ...tfForm, min_len: e.target.value })} />
          <TextField label="Hours" value={tfForm.hours} onChange={(e) => setTfForm({ ...tfForm, hours: e.target.value })} />
          <TextField label="Lookback" value={tfForm.lookback} onChange={(e) => setTfForm({ ...tfForm, lookback: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>History Limit</TableCell>
              <TableCell>Min Len</TableCell>
              <TableCell>Hours</TableCell>
              <TableCell>Lookback</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {timeframes.map(tf => (
              <TableRow key={tf.code}>
                <TableCell>{tf.code}</TableCell>
                <TableCell>{tf.history_limit}</TableCell>
                <TableCell>{tf.min_len}</TableCell>
                <TableCell>{tf.hours}</TableCell>
                <TableCell>{tf.lookback}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeTimeframe(tf.code)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Commands ---- */}
      <TabPanel value={tab} index={1}>
        <form onSubmit={addCommand} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Command" value={cmdForm.command} onChange={(e) => setCmdForm({ ...cmdForm, command: e.target.value })} />
          <TextField label="Group" value={cmdForm.group_name} onChange={(e) => setCmdForm({ ...cmdForm, group_name: e.target.value })} />
          <TextField label="Description" value={cmdForm.description} onChange={(e) => setCmdForm({ ...cmdForm, description: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Command</TableCell>
              <TableCell>Group</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {commands.map(cmd => (
              <TableRow key={cmd.id}>
                <TableCell>{cmd.id}</TableCell>
                <TableCell>{cmd.command}</TableCell>
                <TableCell>{cmd.group_name}</TableCell>
                <TableCell>{cmd.description}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeCommand(cmd.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Reasons ---- */}
      <TabPanel value={tab} index={2}>
        <form onSubmit={addReason} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Code" value={reasonForm.code} onChange={(e) => setReasonForm({ ...reasonForm, code: e.target.value })} />
          <TextField label="Description" value={reasonForm.description} onChange={(e) => setReasonForm({ ...reasonForm, description: e.target.value })} />
          <TextField label="Category" value={reasonForm.category} onChange={(e) => setReasonForm({ ...reasonForm, category: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Category</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reasons.map(r => (
              <TableRow key={r.code}>
                <TableCell>{r.code}</TableCell>
                <TableCell>{r.description}</TableCell>
                <TableCell>{r.category}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeReason(r.code)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Trade Profiles ---- */}
      <TabPanel value={tab} index={3}>
        <form onSubmit={addProfile} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Name" value={profileForm.name} onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })} />
          <TextField label="Description" value={profileForm.description} onChange={(e) => setProfileForm({ ...profileForm, description: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {profiles.map(p => (
              <TableRow key={p.id}>
                <TableCell>{p.id}</TableCell>
                <TableCell>{p.name}</TableCell>
                <TableCell>{p.description}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeProfile(p.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Trade Conditions ---- */}
      <TabPanel value={tab} index={4}>
        <form onSubmit={addCondition} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Profile ID" value={conditionForm.profile_id} onChange={(e) => setConditionForm({ ...conditionForm, profile_id: e.target.value })} />
          <TextField label="Action" value={conditionForm.action} onChange={(e) => setConditionForm({ ...conditionForm, action: e.target.value })} />
          <TextField label="Condition Type" value={conditionForm.condition_type} onChange={(e) => setConditionForm({ ...conditionForm, condition_type: e.target.value })} />
          <TextField label="Param 1" value={conditionForm.param_1} onChange={(e) => setConditionForm({ ...conditionForm, param_1: e.target.value })} />
          <TextField label="Param 2" value={conditionForm.param_2} onChange={(e) => setConditionForm({ ...conditionForm, param_2: e.target.value })} />
          <TextField label="Priority" value={conditionForm.priority} onChange={(e) => setConditionForm({ ...conditionForm, priority: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Profile ID</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Condition Type</TableCell>
              <TableCell>Param1</TableCell>
              <TableCell>Param2</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {conditions.map(c => (
              <TableRow key={c.id}>
                <TableCell>{c.id}</TableCell>
                <TableCell>{c.profile_id}</TableCell>
                <TableCell>{c.action}</TableCell>
                <TableCell>{c.condition_type}</TableCell>
                <TableCell>{c.param_1}</TableCell>
                <TableCell>{c.param_2}</TableCell>
                <TableCell>{c.priority}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeCondition(c.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Group Icons ---- */}
      <TabPanel value={tab} index={5}>
        <form onSubmit={addIcon} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Group Name" value={iconForm.group_name} onChange={(e) => setIconForm({ ...iconForm, group_name: e.target.value })} />
          <TextField label="Icon" value={iconForm.icon} onChange={(e) => setIconForm({ ...iconForm, icon: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Group Name</TableCell>
              <TableCell>Icon</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {icons.map(ic => (
              <TableRow key={ic.group_name}>
                <TableCell>{ic.group_name}</TableCell>
                <TableCell>{ic.icon}</TableCell>
                <TableCell align="right">
                  <Button color="error" startIcon={<Delete />} onClick={() => removeIcon(ic.group_name)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>
    </div>
  );
}
