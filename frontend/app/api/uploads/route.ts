import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
    const data = await request.formData()
    const file = data.get('file')
    if (!(file instanceof File)) {
        return NextResponse.json({ success: false, error: "no file" }, { status: 400 })
    }

    const forward = new FormData()
    forward.append('file', file, file.name)

    const backendUrl = process.env.BACKEND_URL ?? 'http://backend:8000'
    const res = await fetch(`${backendUrl}/uploads`, { method: 'POST', body: forward })

    if (!res.ok) {
        return NextResponse.json({ success: false }, { status: 502 })
    }
    return NextResponse.json(await res.json())
}