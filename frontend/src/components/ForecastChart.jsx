import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip
} from "recharts";

export default function ForecastChart({
    data
}) {
    return (
        <ResponsiveContainer
            width="100%"
            height={320}
        >
            <LineChart data={data}>
                <XAxis
                    dataKey="date"
                    tickLine={false}
                    axisLine={false}
                />

                <YAxis
                    tickLine={false}
                    axisLine={false}
                />
                <Tooltip />

                <Line
                    type="monotone"
                    dataKey="predicted_revenue"
                    stroke="#E06A27"
                    strokeWidth={3}
                    dot={false}
                />
            </LineChart>
        </ResponsiveContainer>
    );
}