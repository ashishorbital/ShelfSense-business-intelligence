import { useState } from "react";
import api from "../api";

export default function CLV() {

    const [customerId, setCustomerId] = useState("");
    const [customer, setCustomer] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const searchCustomer = async () => {

        if (!customerId.trim()) {
            setError("Please enter a Customer ID");
            setCustomer(null);
            return;
        }

        try {

            setLoading(true);
            setError("");

            const res = await api.get(
                `/clv/${customerId}`
            );

            if (!res.data?.found) {

                setCustomer(null);

                setError(
                    res.data?.message ||
                    "Customer ID not found"
                );

                return;
            }

            setCustomer(res.data);
            setError("");

        } catch (err) {

            console.error(err);

            setCustomer(null);

            setError(
                "Unable to fetch customer information"
            );

        } finally {

            setLoading(false);
        }
    };

    const getTierClass = (tier) => {

        if (tier === "High") return "tier-high";

        if (tier === "Medium")
            return "tier-medium";

        return "tier-low";
    };

    return (

        <div className="clv-page">

            <div className="page-header">

                <p className="eyebrow">
                    Customer Intelligence
                </p>

                <h1>
                    Customer Value
                </h1>

                <p className="hero-copy">
                    Analyze customer lifetime value and
                    purchasing behavior using machine
                    learning predictions.
                </p>

            </div>

            <div className="search-panel section-card">

                <input
                    type="number"
                    placeholder="Enter Customer ID"
                    value={customerId}
                    onChange={(e) =>
                        setCustomerId(
                            e.target.value
                        )
                    }
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            searchCustomer();
                        }
                    }}
                />

                <button
                    onClick={searchCustomer}
                    disabled={loading}
                >
                    {loading
                        ? "Loading..."
                        : "Analyze Customer"}
                </button>

            </div>

            {error && (

                <div className="error-card">

                    {error}

                </div>

            )}

            {customer?.found && (

                <>

                    <div className="customer-profile section-card">

                        <div>

                            <span className="profile-label">
                                Customer ID
                            </span>

                            <h2>
                                {customer.customer_id}
                            </h2>

                        </div>

                        <div>

                            <span className="profile-label">
                                Customer Tier
                            </span>

                            <div
                                className={`tier-badge ${getTierClass(
                                    customer.tier
                                )}`}
                            >
                                {customer.tier}
                            </div>

                        </div>

                    </div>

                    <div className="customer-metrics">

                        <div className="profile-card">

                            <span>
                                Predicted CLV
                            </span>

                            <h3>
                                £
                                {customer.predicted_clv.toLocaleString()}
                            </h3>

                        </div>

                        <div className="profile-card">

                            <span>
                                Revenue
                            </span>

                            <h3>
                                £
                                {customer.total_revenue.toLocaleString()}
                            </h3>

                        </div>

                        <div className="profile-card">

                            <span>
                                Orders
                            </span>

                            <h3>
                                {customer.purchase_frequency}
                            </h3>

                        </div>

                        <div className="profile-card">

                            <span>
                                Avg Order Value
                            </span>

                            <h3>
                                £
                                {customer.avg_order_value.toLocaleString()}
                            </h3>

                        </div>

                        <div className="profile-card">

                            <span>
                                Products Bought
                            </span>

                            <h3>
                                {customer.unique_products}
                            </h3>

                        </div>

                        <div className="profile-card">

                            <span>
                                Days Since Last Purchase
                            </span>

                            <h3>
                                {customer.days_since_last_purchase}
                            </h3>

                        </div>

                    </div>

                </>

            )}

        </div>

    );
}