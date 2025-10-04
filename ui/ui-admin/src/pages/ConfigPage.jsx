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
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from "@mui/material";
import { Add, Delete } from "@mui/icons-material";

import {
  getTimeframes, createTimeframe, updateTimeframe, deleteTimeframe,
  getCommands, createCommand, updateCommand, deleteCommand,
  getReasons, createReason, updateReason, deleteReason,
  getTradeProfiles, createTradeProfile, updateTradeProfile, deleteTradeProfile,
  getTradeConditions, createTradeCondition, updateTradeCondition, deleteTradeCondition,
  getGroupIcons, createGroupIcon, updateGroupIcon, deleteGroupIcon,
  getSettings, createSetting, updateSetting, deleteSetting
} from "../api/config";
import { getExchanges } from "../api/exchanges";

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
}

export default function PageConfig() {
  const [tab, setTab] = useState(0);

  // ---- Settings ----
  const [settings, setSettings] = useState([]);
  const [settingForm, setSettingForm] = useState({
    service_name: "",
    key: "",
    value: "",
    value_type: "str",
  });

  async function loadSettings() { setSettings(await getSettings()); }
  async function addSetting(e) {
    e.preventDefault();
    const payload = {
      service_name: settingForm.service_name,
      key: settingForm.key,
      value: settingForm.value,
      value_type: settingForm.value_type || "str"
    };
    await createSetting(payload);
    setSettingForm({ service_name: "", key: "", value: "", value_type: "str" });
    loadSettings();
  }
  async function saveSetting(s) {
    const payload = { ...s, value_type: s.value_type || "str" };
    await updateSetting(s.id, payload);
    loadSettings();
  }
  async function removeSetting(id) {
    if (window.confirm("Видалити setting?")) {
      await deleteSetting(id);
      loadSettings();
    }
  }

  // ---- Timeframes ----
  const [timeframes, setTimeframes] = useState([]);
  const [tfForm, setTfForm] = useState({ code: "", history_limit: "", min_len: "", hours: "" });
  const [exchanges, setExchanges] = useState([]);
  const [selectedExchange, setSelectedExchange] = useState("");

  async function loadExchanges() {
    const data = await getExchanges();
    console.log("🔍 Exchanges loaded:", data);
    setExchanges(data || []);
    if (data && data.length > 0 && !selectedExchange) {
      setSelectedExchange(data[0].id);
    }
  }

  useEffect(() => {
    if (selectedExchange) loadTimeframes(selectedExchange);
  }, [selectedExchange]);

  async function loadTimeframes(exchangeId) {
    const data = await getTimeframes(exchangeId);
    setTimeframes(data);
  }
  async function addTimeframe(e) {
    e.preventDefault();
    const payload = {
      code: tfForm.code,
      history_limit: tfForm.history_limit ? parseInt(tfForm.history_limit, 10) : null,
      min_len: tfForm.min_len ? parseInt(tfForm.min_len, 10) : null,
      hours: tfForm.hours ? parseFloat(tfForm.hours) : null,
      exchange_id: selectedExchange,
    };
    await createTimeframe(payload);
    setTfForm({ code: "", history_limit: "", min_len: "", hours: "" });
    loadTimeframes(selectedExchange);
  }
  async function saveTimeframe(tf) {
    const payload = {
      code: tf.code,
      history_limit: parseInt(tf.history_limit, 10),
      min_len: parseInt(tf.min_len, 10),
      hours: parseFloat(tf.hours),
      exchange_id: tf.exchange_id,
    };
    await updateTimeframe(tf.code, payload);
//    loadTimeframes();
    loadTimeframes(selectedExchange);
  }

  async function removeTimeframe(tf) {
    if (window.confirm("Видалити таймфрейм?")) {
      await deleteTimeframe(tf.code, tf.exchange_id);
      loadTimeframes(selectedExchange);
    }
  }

  const filteredTimeframes = timeframes.filter(tf => tf.exchange_id === selectedExchange);

  useEffect(() => {
    (async () => {
      const data = await getExchanges();
      console.log("🔍 Exchanges loaded:", data);
      setExchanges(data || []);
      if (data && data.length > 0) {
        const firstEx = data[0].id;
        setSelectedExchange(firstEx);
        await loadTimeframes(firstEx);
      }
    })();
  }, []);

  // ---- Commands ----
  const [commands, setCommands] = useState([]);
  const [cmdForm, setCmdForm] = useState({ command: "", group_name: "", description: "" });

  async function loadCommands() { setCommands(await getCommands()); }
  async function addCommand(e) {
    e.preventDefault();
    const payload = {
      command: cmdForm.command,
      group_name: cmdForm.group_name,
      description: cmdForm.description || ""
    };
    await createCommand(payload);
    setCmdForm({ command: "", group_name: "", description: "" });
    loadCommands();
  }
  async function saveCommand(cmd) {
    const payload = { id: cmd.id, command: cmd.command, group_name: cmd.group_name, description: cmd.description || "" };
    await updateCommand(cmd.id, payload);
    loadCommands();
  }
  async function removeCommand(id) {
    if (window.confirm("Видалити команду?")) {
      await deleteCommand(id);
      loadCommands();
    }
  }

  // ---- Reasons ----
  const [reasons, setReasons] = useState([]);
  const [reasonForm, setReasonForm] = useState({ code: "", description: "", category: "" });

  async function loadReasons() { setReasons(await getReasons()); }
  async function addReason(e) {
    e.preventDefault();
    const payload = {
      code: reasonForm.code,
      description: reasonForm.description || "",
      category: reasonForm.category || "MANUAL"
    };
    await createReason(payload);
    setReasonForm({ code: "", description: "", category: "" });
    loadReasons();
  }
  async function saveReason(r) {
    const payload = { code: r.code, description: r.description || "", category: r.category || "MANUAL" };
    await updateReason(r.code, payload);
    loadReasons();
  }
  async function removeReason(code) {
    if (window.confirm("Видалити reason?")) {
      await deleteReason(code);
      loadReasons();
    }
  }

  // ---- Trade Profiles ----
  const [profiles, setProfiles] = useState([]);
  const [profileForm, setProfileForm] = useState({ user_id: "", exchange_id: "", name: "", description: "" });

  async function loadProfiles() {
    const data = await getTradeProfiles();
    setProfiles(data.map((p) => ({
      id: p.id,
      user_id: p.user_id || p.userId,
      exchange_id: p.exchange_id || p.exchangeId,
      name: p.name,
      description: p.description
    })));
  }
  async function addProfile(e) {
    e.preventDefault();
    const payload = {
      user_id: profileForm.user_id,
      exchange_id: profileForm.exchange_id,
      name: profileForm.name,
      description: profileForm.description || ""
    };
    await createTradeProfile(payload);
    setProfileForm({ user_id: "", exchange_id: "", name: "", description: "" });
    loadProfiles();
  }
  async function saveProfile(p) {
    const payload = { id: p.id, user_id: p.user_id, exchange_id: p.exchange_id, name: p.name, description: p.description || "" };
    await updateTradeProfile(p.id, payload);
    loadProfiles();
  }
  async function removeProfile(id) {
    if (window.confirm("Видалити профіль?")) {
      await deleteTradeProfile(id);
      loadProfiles();
    }
  }

  // ---- Trade Conditions ----
  const [conditions, setConditions] = useState([]);
  const [conditionForm, setConditionForm] = useState({
    profile_id: "", action: "", condition_type: "", param_1: "", param_2: "", priority: "",
  });

  async function loadConditions() { setConditions(await getTradeConditions()); }
  async function addCondition(e) {
    e.preventDefault();
    const payload = {
      profile_id: parseInt(conditionForm.profile_id, 10),
      action: conditionForm.action,
      condition_type: conditionForm.condition_type,
      param_1: conditionForm.param_1 ? parseFloat(conditionForm.param_1) : null,
      param_2: conditionForm.param_2 ? parseFloat(conditionForm.param_2) : null,
      priority: parseInt(conditionForm.priority, 10)
    };
    await createTradeCondition(payload);
    setConditionForm({ profile_id: "", action: "", condition_type: "", param_1: "", param_2: "", priority: "" });
    loadConditions();
  }
  async function saveCondition(c) {
    const payload = {
      id: c.id,
      profile_id: parseInt(c.profile_id, 10),
      action: c.action,
      condition_type: c.condition_type,
      param_1: c.param_1 ? parseFloat(c.param_1) : null,
      param_2: c.param_2 ? parseFloat(c.param_2) : null,
      priority: parseInt(c.priority, 10)
    };
    await updateTradeCondition(c.id, payload);
    loadConditions();
  }
  async function removeCondition(id) {
    if (window.confirm("Видалити condition?")) {
      await deleteTradeCondition(id);
      loadConditions();
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
  async function saveIcon(ic) { await updateGroupIcon(ic.group_name, ic); loadIcons(); }
  async function removeIcon(name) {
    if (window.confirm("Видалити іконку?")) {
      await deleteGroupIcon(name);
      loadIcons();
    }
  }

  // ---- Lifecycle ----
  useEffect(() => {
    loadSettings();
    loadCommands();
    loadReasons();
    loadProfiles();
    loadConditions();
    loadIcons();
    loadExchanges();
  }, []);

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Core Config</h1>
      <Paper>
        <Tabs value={tab} onChange={(e, v) => setTab(v)} indicatorColor="primary" textColor="primary">
          <Tab label="Settings" />
          <Tab label="Timeframes" />
          <Tab label="Commands" />
          <Tab label="Reasons" />
          <Tab label="Trade Profiles" />
          <Tab label="Trade Conditions" />
          <Tab label="Group Icons" />
        </Tabs>
      </Paper>

      {/* ---- Settings ---- */}
      <TabPanel value={tab} index={0}>
        <form onSubmit={addSetting} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="Service Name" value={settingForm.service_name} onChange={(e) => setSettingForm({ ...settingForm, service_name: e.target.value })} />
          <TextField label="Key" value={settingForm.key} onChange={(e) => setSettingForm({ ...settingForm, key: e.target.value })} />
          <TextField label="Value" value={settingForm.value} onChange={(e) => setSettingForm({ ...settingForm, value: e.target.value })} />
          <FormControl>
            <InputLabel>Value Type</InputLabel>
            <Select
              value={settingForm.value_type}
              onChange={(e) => setSettingForm({ ...settingForm, value_type: e.target.value })}
              style={{ minWidth: 120 }}
            >
              <MenuItem value="str">text (str)</MenuItem>
              <MenuItem value="json">json</MenuItem>
              <MenuItem value="float">float</MenuItem>
              <MenuItem value="int">int</MenuItem>
            </Select>
          </FormControl>
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Service</TableCell>
              <TableCell>Key</TableCell>
              <TableCell>Value</TableCell>
              <TableCell>Value Type</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {settings.map((s) => (
              <TableRow key={s.id}>
                <TableCell>{s.service_name}</TableCell>
                <TableCell>
                  <TextField
                    value={s.key || ""}
                    size="small"
                    onChange={(e) =>
                      setSettings((prev) =>
                        prev.map((x) =>
                          x.id === s.id ? { ...x, key: e.target.value } : x
                        )
                      )
                    }
                  />
                </TableCell>
                <TableCell>
                  <TextField
                    value={s.value || ""}
                    size="small"
                    onChange={(e) =>
                      setSettings((prev) =>
                        prev.map((x) =>
                          x.id === s.id ? { ...x, value: e.target.value } : x
                        )
                      )
                    }
                  />
                </TableCell>
                <TableCell>
                  <FormControl size="small" fullWidth>
                    <Select
                      value={s.value_type || "str"}
                      onChange={(e) =>
                        setSettings((prev) =>
                          prev.map((x) =>
                            x.id === s.id ? { ...x, value_type: e.target.value } : x
                          )
                        )
                      }
                    >
                      <MenuItem value="str">str</MenuItem>
                      <MenuItem value="int">int</MenuItem>
                      <MenuItem value="float">float</MenuItem>
                      <MenuItem value="json">json</MenuItem>
                    </Select>
                  </FormControl>
                </TableCell>
                <TableCell align="right">
                  <Button
                    size="small"
                    variant="contained"
                    onClick={() => saveSetting(s)}
                  >
                    Зберегти
                  </Button>
                  <Button
                    size="small"
                    color="error"
                    startIcon={<Delete />}
                    onClick={() => removeSetting(s.id)}
                  >
                    Видалити
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Timeframes ---- */}
      <TabPanel value={tab} index={1}>
        {/* --- Select Exchange --- */}
        <FormControl fullWidth style={{ marginBottom: 16 }}>
          <InputLabel>Exchange</InputLabel>
          <Select
            value={selectedExchange}
            onChange={(e) => setSelectedExchange(e.target.value)}
          >
            {exchanges.map((ex) => (
              <MenuItem key={ex.id} value={ex.id}>
                {ex.code.toUpperCase()}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* --- Add Form --- */}
        <form
          onSubmit={addTimeframe}
          style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}
        >
          <TextField
            label="Code"
            value={tfForm.code}
            onChange={(e) => setTfForm({ ...tfForm, code: e.target.value })}
          />
          <TextField
            label="History Limit"
            value={tfForm.history_limit}
            onChange={(e) => setTfForm({ ...tfForm, history_limit: e.target.value })}
          />
          <TextField
            label="Min Len"
            value={tfForm.min_len}
            onChange={(e) => setTfForm({ ...tfForm, min_len: e.target.value })}
          />
          <TextField
            label="Hours"
            value={tfForm.hours}
            onChange={(e) => setTfForm({ ...tfForm, hours: e.target.value })}
          />
          <Button type="submit" variant="contained" startIcon={<Add />}>
            Додати
          </Button>
        </form>

        {/* --- Table --- */}
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>History Limit</TableCell>
              <TableCell>Min Len</TableCell>
              <TableCell>Hours</TableCell>
              <TableCell>Exchange</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredTimeframes.map((tf) => (
              <TableRow key={`${tf.code}-${tf.exchange_id}`}>
                <TableCell>{tf.code}</TableCell>
                <TableCell>
                  <TextField
                    value={tf.history_limit || ""}
                    size="small"
                    onChange={(e) =>
                      setTimeframes((prev) =>
                        prev.map((t) =>
                          t.code === tf.code && t.exchange_id === tf.exchange_id
                            ? { ...t, history_limit: e.target.value }
                            : t
                        )
                      )
                    }
                  />
                </TableCell>
                <TableCell>
                  <TextField
                    value={tf.min_len || ""}
                    size="small"
                    onChange={(e) =>
                      setTimeframes((prev) =>
                        prev.map((t) =>
                          t.code === tf.code && t.exchange_id === tf.exchange_id
                            ? { ...t, min_len: e.target.value }
                            : t
                        )
                      )
                    }
                  />
                </TableCell>
                <TableCell>
                  <TextField
                    value={tf.hours || ""}
                    size="small"
                    onChange={(e) =>
                      setTimeframes((prev) =>
                        prev.map((t) =>
                          t.code === tf.code && t.exchange_id === tf.exchange_id
                            ? { ...t, hours: e.target.value }
                            : t
                        )
                      )
                    }
                  />
                </TableCell>
                <TableCell>
                  {exchanges.find((ex) => ex.id === tf.exchange_id)?.code || "—"}
                </TableCell>
                <TableCell align="right">
                  <Button
                    size="small"
                    variant="contained"
                    onClick={() => saveTimeframe(tf)}
                  >
                    Зберегти
                  </Button>
                  <Button
                    size="small"
                    color="error"
                    startIcon={<Delete />}
                    onClick={() => removeTimeframe(tf)}
                  >
                    Видалити
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Commands ---- */}
      <TabPanel value={tab} index={2}>
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
            {commands.map((cmd) => (
              <TableRow key={cmd.id}>
                <TableCell>{cmd.id}</TableCell>
                <TableCell>
                  <TextField value={cmd.command || ""} size="small" onChange={(e) => setCommands(prev => prev.map(c => c.id === cmd.id ? { ...c, command: e.target.value } : c))} />
                </TableCell>
                <TableCell>
                  <TextField value={cmd.group_name || ""} size="small" onChange={(e) => setCommands(prev => prev.map(c => c.id === cmd.id ? { ...c, group_name: e.target.value } : c))} />
                </TableCell>
                <TableCell>
                  <TextField value={cmd.description || ""} size="small" onChange={(e) => setCommands(prev => prev.map(c => c.id === cmd.id ? { ...c, description: e.target.value } : c))} />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" variant="contained" onClick={() => saveCommand(cmd)}>Зберегти</Button>
                  <Button size="small" color="error" startIcon={<Delete />} onClick={() => removeCommand(cmd.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Reasons ---- */}
      <TabPanel value={tab} index={3}>
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
            {reasons.map((r) => (
              <TableRow key={r.code}>
                <TableCell>{r.code}</TableCell>
                <TableCell>
                  <TextField value={r.description || ""} size="small" onChange={(e) => setReasons(prev => prev.map(x => x.code === r.code ? { ...x, description: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={r.category || ""} size="small" onChange={(e) => setReasons(prev => prev.map(x => x.code === r.code ? { ...x, category: e.target.value } : x))} />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" variant="contained" onClick={() => saveReason(r)}>Зберегти</Button>
                  <Button size="small" color="error" startIcon={<Delete />} onClick={() => removeReason(r.code)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Trade Profiles ---- */}
      <TabPanel value={tab} index={4}>
        <form onSubmit={addProfile} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <TextField label="UserID" value={profileForm.user_id} onChange={(e) => setProfileForm({ ...profileForm, user_id: e.target.value })} />
          <TextField label="ExchangeID" value={profileForm.exchange_id} onChange={(e) => setProfileForm({ ...profileForm, exchange_id: e.target.value })} />
          <TextField label="Name" value={profileForm.name} onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })} />
          <TextField label="Description" value={profileForm.description} onChange={(e) => setProfileForm({ ...profileForm, description: e.target.value })} />
          <Button type="submit" variant="contained" startIcon={<Add />}>Додати</Button>
        </form>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>UserID</TableCell>
              <TableCell>ExchangeID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {profiles.map((p) => (
              <TableRow key={p.id}>
                <TableCell>{p.id}</TableCell>
                <TableCell>
                  <TextField value={p.user_id || ""} size="small" onChange={(e) => setProfiles(prev => prev.map(x => x.id === p.id ? { ...x, user_id: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={p.exchange_id || ""} size="small" onChange={(e) => setProfiles(prev => prev.map(x => x.id === p.id ? { ...x, exchange_id: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={p.name || ""} size="small" onChange={(e) => setProfiles(prev => prev.map(x => x.id === p.id ? { ...x, name: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={p.description || ""} size="small" onChange={(e) => setProfiles(prev => prev.map(x => x.id === p.id ? { ...x, description: e.target.value } : x))} />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" variant="contained" onClick={() => saveProfile(p)}>Зберегти</Button>
                  <Button size="small" color="error" startIcon={<Delete />} onClick={() => removeProfile(p.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Trade Conditions ---- */}
      <TabPanel value={tab} index={5}>
        <form onSubmit={addCondition} style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
          <TextField label="Profile ID" value={conditionForm.profile_id} onChange={(e) => setConditionForm({ ...conditionForm, profile_id: e.target.value })} />
          <TextField label="Action" value={conditionForm.action} onChange={(e) => setConditionForm({ ...conditionForm, action: e.target.value })} />
          <TextField label="Condition Type" value={conditionForm.condition_type} onChange={(e) => setConditionForm({ ...conditionForm, condition_type: e.target.value })} />
          <TextField label="Param1" value={conditionForm.param_1} onChange={(e) => setConditionForm({ ...conditionForm, param_1: e.target.value })} />
          <TextField label="Param2" value={conditionForm.param_2} onChange={(e) => setConditionForm({ ...conditionForm, param_2: e.target.value })} />
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
            {conditions.map((c) => (
              <TableRow key={c.id}>
                <TableCell>{c.id}</TableCell>
                <TableCell>
                  <TextField value={c.profile_id || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, profile_id: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={c.action || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, action: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={c.condition_type || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, condition_type: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={c.param_1 || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, param_1: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={c.param_2 || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, param_2: e.target.value } : x))} />
                </TableCell>
                <TableCell>
                  <TextField value={c.priority || ""} size="small" onChange={(e) => setConditions(prev => prev.map(x => x.id === c.id ? { ...x, priority: e.target.value } : x))} />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" variant="contained" onClick={() => saveCondition(c)}>Зберегти</Button>
                  <Button size="small" color="error" startIcon={<Delete />} onClick={() => removeCondition(c.id)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      {/* ---- Group Icons ---- */}
      <TabPanel value={tab} index={6}>
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
            {icons.map((ic) => (
              <TableRow key={ic.group_name}>
                <TableCell>{ic.group_name}</TableCell>
                <TableCell>
                  <TextField value={ic.icon || ""} size="small" onChange={(e) => setIcons(prev => prev.map(x => x.group_name === ic.group_name ? { ...x, icon: e.target.value } : x))} />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" variant="contained" onClick={() => saveIcon(ic)}>Зберегти</Button>
                  <Button size="small" color="error" startIcon={<Delete />} onClick={() => removeIcon(ic.group_name)}>Видалити</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>
    </div>
  );
}
