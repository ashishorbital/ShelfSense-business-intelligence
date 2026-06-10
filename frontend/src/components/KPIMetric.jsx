export default function KPIMetric({
    value,
    label
}) {
    return (
        <div className="metric">
            <h2>{value}</h2>
            <span>{label}</span>
        </div>
    );
}