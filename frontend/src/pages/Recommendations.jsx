import { useState, useEffect } from "react";
import api from "../api";

export default function Recommendations() {

    const [product, setProduct] = useState("");
    const [products, setProducts] = useState([]);
    const [filteredProducts, setFilteredProducts] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [results, setResults] = useState([]);

    useEffect(() => {

        api
            .get("/products")
            .then((res) => {

                setProducts(res.data);

            })
            .catch((err) => {

                console.error(
                    "Failed to load products",
                    err
                );

            });

    }, []);

    const handleSearchInput = (value) => {

        setProduct(value);

        if (!value.trim()) {

            setFilteredProducts([]);
            setShowDropdown(false);

            return;
        }

        const matches = products
            .filter((p) =>
                p
                    .toLowerCase()
                    .includes(
                        value.toLowerCase()
                    )
            )
            .slice(0, 8);

        setFilteredProducts(matches);

        setShowDropdown(true);
    };

    const selectProduct = (item) => {

        setProduct(item);

        setShowDropdown(false);
    };

    const searchRecommendations = async () => {

        if (!product.trim()) return;

        try {

            const res = await api.get(
                `/recommendations/${encodeURIComponent(product)}`
            );

            setResults(res.data);

        } catch (err) {

            console.error(err);

            alert(
                "No recommendations found"
            );

            setResults([]);
        }
    };

    return (
        <div className="recommendation-page">

            <div className="page-header">

                <p className="eyebrow">
                    Basket Intelligence
                </p>

                <h1>
                    Product Recommendations
                </h1>

                <p className="hero-copy">
                    Discover products frequently
                    purchased together using
                    association rule mining.
                </p>

            </div>

            <div className="search-panel section-card">

                <div className="product-search">

                    <input
                        type="text"
                        placeholder="Search products..."
                        value={product}
                        onChange={(e) =>
                            handleSearchInput(
                                e.target.value
                            )
                        }
                    />

                    {showDropdown &&
                        filteredProducts.length > 0 && (

                            <div className="search-dropdown">

                                {filteredProducts.map(
                                    (item) => (

                                        <div
                                            key={item}
                                            className="search-option"
                                            onClick={() =>
                                                selectProduct(
                                                    item
                                                )
                                            }
                                        >
                                            {item}
                                        </div>

                                    )
                                )}

                            </div>

                        )}

                </div>

                <button
                    onClick={
                        searchRecommendations
                    }
                >
                    Find Recommendations
                </button>

            </div>

            {results.length > 0 && (

                <div className="recommendation-grid">

                    {results.map(
                        (item, index) => (

                            <div
                                key={index}
                                className="recommendation-card section-card"
                            >

                                <div className="recommendation-header">

                                    <div className="recommendation-rank">
                                        #{index + 1}
                                    </div>

                                    <div>

                                        <h3>
                                            {item.product}
                                        </h3>

                                        <p>
                                            Frequently
                                            purchased
                                            together
                                        </p>

                                    </div>

                                </div>

                                <div className="recommendation-stats">

                                    <div>

                                        <span>
                                            Confidence
                                        </span>

                                        <strong>
                                            {(
                                                item.confidence *
                                                100
                                            ).toFixed(
                                                1
                                            )}
                                            %
                                        </strong>

                                    </div>

                                    <div>

                                        <span>
                                            Lift
                                        </span>

                                        <strong>
                                            {
                                                item.lift
                                            }
                                        </strong>

                                    </div>

                                    <div>

                                        <span>
                                            Support
                                        </span>

                                        <strong>
                                            {item.support
                                                ? `${(
                                                    item.support *
                                                    100
                                                ).toFixed(
                                                    2
                                                )}%`
                                                : "N/A"}
                                        </strong>

                                    </div>

                                </div>

                                <div className="confidence-bar">

                                    <div
                                        className="confidence-fill"
                                        style={{
                                            width: `${item.confidence * 100}%`
                                        }}
                                    />

                                </div>

                            </div>

                        )
                    )}

                </div>

            )}

        </div>
    );
}