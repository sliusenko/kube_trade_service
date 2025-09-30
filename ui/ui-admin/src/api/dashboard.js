// src/api/dashboard.js
// Mock API для Dashboard

export const getDashboardStats = async () => {
  // Імітація затримки запиту (щоб виглядало реальніше)
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    exchanges: { active: 3, inactive: 1 },
    serviceAccounts: 5,
    symbolsPerExchange: { BINANCE: 1200, KRAKEN: 400, COINBASE: 250 },
    fetchResults: {
      overall: [
        { type: "Success", value: 150 },
        { type: "Fail", value: 20 }
      ],
      byType: [
        { type: "symbols", success: 80, fail: 10 },
        { type: "limits", success: 40, fail: 5 },
        { type: "fees", success: 20, fail: 3 },
        { type: "price", success: 10, fail: 2 }
      ]
    },
    users: [
      { status: "Active", value: 10 },
      { status: "Inactive", value: 3 }
    ]
  };
};
