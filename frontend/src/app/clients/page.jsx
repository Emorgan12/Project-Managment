"use client"

import React, { useEffect, useState } from "react";
const BaseURL = 'http://127.0.0.1:8000/'

export default function Clients() {
    const [clients, setClients] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function getClients() {
            try {
                const res = await fetch(`${BaseURL}get-clients/`);
                if (!res.ok) throw new Error(`Request failed: ${res.status}`);
                setClients(await res.json());
            } catch (err) {
                setError(err.message);
            }
        }
        getClients();
    }, []);

    const fullName = (c) =>
        [c.first_name, c.middle_name, c.last_name].filter(Boolean).join(" ");

    return (
        <div className="flex flex-col flex-1 items-center mt-10">
            {error && <p className="text-red-500">Could not load clients: {error}</p>}
            <table className="text-center w-auto bg-gray-300 border-4 [&_th]:px-6 [&_th]:py-3 [&_td]:px-6 [&_td]:py-3">
                <thead>
                    <tr className="border-4">
                        <th className="border-2">Name</th>
                        <th className="border-2">Contact</th>
                        <th className="border-2">Company</th>
                    </tr>
                </thead>
                <tbody>
                    {clients.map((c) => (
                        <tr key={c.id}>
                            <td className="border-2">{fullName(c)}</td>
                            <td className="border-2">{c.client_email}</td>
                            <td className="border-2">{c.company}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
