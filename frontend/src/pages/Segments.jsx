import { useEffect, useState } from "react";
import api from "../api";

export default function Segments() {

    const [segments, setSegments] = useState([]);

    useEffect(() => {

        api
            .get("/segment-analytics")
            .then((res) =>
                setSegments(res.data)
            );

    }, []);

    return (
        <div className="segments-page">

            <div className="page-header">

                <p className="eyebrow">
                    Customer Intelligence
                </p>

                <h1>
                    Customer Segments
                </h1>

                <p className="hero-copy">
                    Understand customer behavior,
                    revenue contribution and
                    engagement across segments.
                </p>

            </div>

            <div className="segment-grid">

                {segments.map((segment) => (

                    <div
                        key={segment.segment}
                        className="segment-card section-card"
                    >

                        <h3>
                            {segment.segment}
                        </h3>

                        <div className="segment-stat">

                            <span>
                                Customers
                            </span>

                            <strong>
                                {segment.customers}
                            </strong>

                        </div>

                        <div className="segment-stat">

                            <span>
                                Avg Revenue
                            </span>

                            <strong>
                                £
                                {Math.round(
                                    segment.avg_revenue
                                ).toLocaleString()}
                            </strong>

                        </div>

                        <div className="segment-stat">

                            <span>
                                Avg Frequency
                            </span>

                            <strong>
                                {segment.avg_frequency}
                            </strong>

                        </div>

                        <div className="segment-stat">

                            <span>
                                Avg Recency
                            </span>

                            <strong>
                                {segment.avg_recency}
                                d
                            </strong>

                        </div>

                    </div>

                ))}

            </div>

            <div className="insights-panel section-card">

                <h2>
                    Executive Insights
                </h2>

                <ul>

                    <li>
                        VIP customers contribute the
                        highest revenue per customer.
                    </li>

                    <li>
                        Regular customers form the
                        majority of the customer base.
                    </li>

                    <li>
                        Low value customers show
                        the highest inactivity.
                    </li>

                    <li>
                        Retention campaigns should
                        focus on converting Regular
                        customers into VIP customers.
                    </li>

                </ul>

            </div>

        </div>
    );
}