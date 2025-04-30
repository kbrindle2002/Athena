import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Toaster, toast } from "sonner";

interface User { id: number; username: string; }

const schema = z.object({
  username: z.string().min(3, "≥ 3 chars"),
  password: z.string().min(4, "≥ 4 chars"),
});

type FormData = z.infer<typeof schema>;

export default function UsersPage() {
  const [token, setToken] = useState<string | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [editing, setEdit] = useState<null | number>(null);

  const {
    register, handleSubmit, reset, formState: { errors, isValid }
  } = useForm<FormData>({ resolver: zodResolver(schema), mode: "onChange" });

  const authz = token ? { Authorization: `Bearer ${token}` } : {};

  /* ── helpers ───────────────────────────────────────────── */
  const refresh = async () => {
    if (!token) return;
    const r = await fetch("http://localhost:8000/users/", { headers: authz });
    if (r.ok) setUsers(await r.json());
  };

  const login = async () => {
    const r = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "admin", password: "admin" }),
    });
    if (!r.ok) return toast.error("Login failed");
    const { access_token } = await r.json();
    setToken(access_token);
  };

  const onSubmit = async (data: FormData) => {
    const method = editing ? "PATCH" : "POST";
    const url = editing
      ? `http://localhost:8000/users/${editing}`
      : "http://localhost:8000/users/";
    const r = await fetch(url, {
      method,
      headers: { ...authz, "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!r.ok) return toast.error("Request failed");
    toast.success(editing ? "User updated" : "User created");
    reset(); setEdit(null); refresh();
  };

  const del = async (id: number) => {
    if (!confirm("Delete user?")) return;
    await fetch(`http://localhost:8000/users/${id}`, {
      method: "DELETE",
      headers: authz,
    });
    toast.success("User deleted");
    refresh();
  };

  useEffect(() => { refresh(); }, [token]);

  /* ── UI ────────────────────────────────────────────────── */
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <Toaster richColors />

      {/* Top bar */}
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-purple-700">ATHENA Users</h1>
        {token ? (
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600 font-medium">admin</span>
            <button
              onClick={() => { setToken(null); setUsers([]); }}
              className="rounded bg-gray-200 px-3 py-1 text-sm hover:bg-gray-300"
            >
              Logout
            </button>
          </div>
        ) : (
          <button
            onClick={login}
            className="rounded bg-purple-600 px-4 py-2 text-white hover:bg-purple-700"
          >
            Admin Login
          </button>
        )}
      </header>

      {/* Form & table only when logged in */}
      {token && (
        <div className="mx-auto max-w-4xl space-y-8">
          {/* Form */}
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="rounded-lg border bg-white p-5 shadow-sm space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <input
                  placeholder="username"
                  className="w-full rounded border px-3 py-2"
                  {...register("username")}
                />
                {errors.username && (
                  <p className="mt-1 text-xs text-red-600">{errors.username.message}</p>
                )}
              </div>
              <div>
                <input
                  type="password"
                  placeholder="password"
                  className="w-full rounded border px-3 py-2"
                  {...register("password")}
                />
                {errors.password && (
                  <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>
                )}
              </div>
            </div>
            <button
              disabled={!isValid}
              className={`rounded px-4 py-2 text-white
                ${isValid ? "bg-emerald-600 hover:bg-emerald-700"
                           : "bg-emerald-300 cursor-not-allowed"}`}
            >
              {editing ? "Update" : "Create"}
            </button>
            {editing && (
              <button
                type="button"
                onClick={() => { setEdit(null); reset(); }}
                className="ml-2 text-sm text-gray-600 underline"
              >
                cancel edit
              </button>
            )}
          </form>

          {/* User table */}
          <div className="overflow-x-auto rounded-lg shadow-sm">
            <table className="min-w-full divide-y divide-gray-200 bg-white text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">ID</th>
                  <th className="px-4 py-2 text-left font-medium">Username</th>
                  <th className="px-4 py-2 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2">{u.id}</td>
                    <td className="px-4 py-2">{u.username}</td>
                    <td className="px-4 py-2 space-x-2 text-center">
                      <button
                        onClick={() => {
                          setEdit(u.id);
                          reset({ username: u.username, password: "" });
                        }}
                        className="rounded bg-yellow-500 px-2 py-1 text-white hover:bg-yellow-600"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => del(u.id)}
                        className="rounded bg-red-600 px-2 py-1 text-white hover:bg-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
                {users.length === 0 && (
                  <tr>
                    <td colSpan={3} className="px-4 py-4 text-center text-gray-500">
                      No users yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
