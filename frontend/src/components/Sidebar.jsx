import { NavLink } from "react-router-dom";

import {
    LayoutDashboard,
    Users,
    BarChart3,
    ShoppingBasket,
    TrendingUp
} from "lucide-react";

export default function Sidebar() {

    const menu = [
        {
            label: "Overview",
            path: "/",
            icon: <LayoutDashboard size={18} />
        },
        {
            label: "Customer Value",
            path: "/clv",
            icon: <Users size={18} />
        },
        {
            label: "Customer Segments",
            path: "/segments",
            icon: <BarChart3 size={18} />
        },
        {
            label: "Basket Analysis",
            path: "/recommendations",
            icon: <ShoppingBasket size={18} />
        },
        {
            label: "Revenue Outlook",
            path: "/forecast",
            icon: <TrendingUp size={18} />
        }
    ];

    return (
        <aside className="sidebar">

            <div className="brand">

                <div className="brand-mark">
                    SS
                </div>

                <div>
                    <h1>ShelfSense</h1>
                    <span>
                        Retail Decision Intelligence
                    </span>
                </div>

            </div>

            <nav className="sidebar-nav">

                {menu.map((item) => (

                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            isActive
                                ? "nav-item active"
                                : "nav-item"
                        }
                    >

                        {item.icon}

                        <span>
                            {item.label}
                        </span>

                    </NavLink>

                ))}

            </nav>

            <div className="sidebar-footer">

                <div className="footer-label">
                    DATA STATUS
                </div>

                <div className="footer-value">
                    Online Retail Dataset
                </div>

            </div>

        </aside>
    );
}