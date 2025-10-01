import React, { useEffect, useState } from "react";
import { Card, CardContent } from "@mui/material";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis
} from "recharts";
import { getDashboardStats } from "../api/dashboard";

const COLORS = ["#0088FE", "#FF8042", "#00C49F", "#FFBB28"];

const DashboardPage = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error("❌ Failed to fetch dashboard stats:", err);
      }
    };
    fetchStats();
  }, []);

  if (!stats) return <div>Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Dashboard</h1>

      {/* Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        <Card><CardContent>
          <h3>Біржі</h3>
          <p>Активні: {stats.exchanges.active}</p>
          <p>Неактивні: {stats.exchanges.inactive}</p>
        </CardContent></Card>

        <Card><CardContent>
          <h3>Сервісні акаунти</h3>
          <p>{stats.serviceAccounts}</p>
        </CardContent></Card>

        <Card><CardContent>
          <h3>Символи по біржах</h3>
          <ul>
            {Object.entries(stats.symbolsPerExchange).map(([ex, count]) => (
              <li key={ex}>{ex}: {count}</li>
            ))}
          </ul>
        </CardContent></Card>
      </div>

      {/* Charts */}
      <div style={{ display: "flex", gap: 40 }}>
        {/* Pie chart for fetch results */}
        <PieChart width={400} height={300}>
          <Pie
            data={stats.fetchResults.overall}
            dataKey="value"
            nameKey="type"
            outerRadius={100}
            label
          >
            {stats.fetchResults.overall.map((entry, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>

        {/* Bar chart for fetch by type */}
        <BarChart width={500} height={300} data={stats.fetchResults.byType}>
          <XAxis dataKey="type" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="success" fill="#00C49F" />
          <Bar dataKey="fail" fill="#FF8042" />
        </BarChart>
      </div>

      {/* Users chart */}
      <PieChart width={400} height={300}>
        <Pie
          data={stats.users}
          dataKey="value"
          nameKey="status"
          outerRadius={100}
          label
        >
          {stats.users.map((entry, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default DashboardPage;
