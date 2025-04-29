import { useEffect, useState } from "react";

interface User {
  id: number;
  username: string;
}

export default function UsersPage() {
  const [token, setToken]   = useState<string | null>(null);
  const [users, setUsers]   = useState<User[]>([]);
  const [form, setForm]     = useState({ username: "", password: "" });
  const [editing, setEdit]  = useState<null | number>(null);

  /** helpers */
  const authz = token ? { Authorization: `Bearer ${token}` } : {};

  async function login() {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "admin", password: "admin" }),
    });
    setToken((await res.json()).access_token);
  }

  async function refresh() {
    if (!token) return;
    const res = await fetch("/users/", { headers: authz });
    setUsers(await res.json());
  }

  async function save() {
    if (!form.username || !form.password) return;
    const method = editing ? "PATCH" : "POST";
    const url    = editing ? `/users/${editing}` : "/users/";
    await fetch(url, {
      method,
      headers: { ...authz, "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setForm({ username: "", password: "" });
    setEdit(null);
    refresh();
  }

  async function del(id: number) {
    await fetch(`/users/${id}`, { method: "DELETE", headers: authz });
    refresh();
  }

  useEffect(() => { if (token) refresh(); }, [token]);

  return (
    <div className="p-6 space-y-6">
      {!token && (
        <button onClick={login} className="px-4 py-2 bg-blue-600 text-white rounded">
          Admin Login
        </button>
      )}

      {token && (
        <>
          {/* form */}
          <div className="space-x-2">
            <input
              className="border rounded px-2 py-1"
              placeholder="username"
              value={form.username}
              onChange={e => setForm({ ...form, username: e.target.value })}
            />
            <input
              className="border rounded px-2 py-1"
              placeholder="password"
              type="password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
            />
            <button onClick={save} className="px-3 py-1 bg-green-600 text-white rounded">
              {editing ? "Update" : "Create"}
            </button>
          </div>

          {/* table */}
          <table className="min-w-full border">
            <thead className="bg-gray-100">
              <tr><th className="px-2 py-1">ID</th><th>Username</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} className="border-t">
                  <td className="px-2">{u.id}</td>
                  <td>{u.username}</td>
                  <td className="space-x-2">
                    <button
                      onClick={() => { setEdit(u.id); setForm({ username: u.username, password: "" }); }}
                      className="px-2 py-0.5 bg-yellow-500 text-white rounded"
                    >
                      edit
                    </button>
                    <button
                      onClick={() => del(u.id)}
                      className="px-2 py-0.5 bg-red-600 text-white rounded"
                    >
                      delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
