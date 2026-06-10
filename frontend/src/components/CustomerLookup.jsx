import { useState } from "react";

export default function CustomerLookup({
    onSearch
}) {

    const [customerId, setCustomerId] = useState("");

    const handleSubmit = (e) => {

        e.preventDefault();

        if (!customerId) return;

        onSearch(customerId);
    };

    return (
        <form
            className="lookup-form"
            onSubmit={handleSubmit}
        >

            <input
                type="number"
                placeholder="Enter Customer ID"
                value={customerId}
                onChange={(e) =>
                    setCustomerId(e.target.value)
                }
            />

            <button type="submit">
                Analyze
            </button>

        </form>
    );
}