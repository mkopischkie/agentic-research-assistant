import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
    const { query } = await request.json()
    if (!query) {
        return NextResponse.json({ error: "no query" }, { status: 400 })
    }

    const backendUrl = process.env.BACKEND_URL ?? 'http://backend:8000'
    const res = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
    })

    if (!res.ok) {
        return NextResponse.json({ error: "backend error" }, { status: 502 })
    }
    return NextResponse.json(await res.json())
}
