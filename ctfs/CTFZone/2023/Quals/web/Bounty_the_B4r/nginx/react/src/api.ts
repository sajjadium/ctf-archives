export class ApiError extends Error {
  code: number

  constructor(code: number, message: string) {
    super(message)
    this.code = code
  }
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

export type ErrorResponse = {
  error: number
  message: string
}

export type LoginResponse = {
  token: string
}

export async function login(
  username: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`/api/user/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })

  if (response.status === 404) {
    throw new ApiError(response.status, "User not found")
  } else if (response.status != 200) {
    const json: ErrorResponse = await response.json()

    throw new ApiError(response.status, json.message)
  }

  const json: LoginResponse = await response.json()

  localStorage.setItem("token", json.token)

  return json
}

export type RegisterResponse = {
  token: string
}

export async function register(
  username: string,
  password: string,
): Promise<RegisterResponse> {
  const response = await fetch(`/api/user/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })

  if (response.status != 200) {
    const json: ErrorResponse = await response.json()

    throw new ApiError(response.status, json.message)
  }

  const json: RegisterResponse = await response.json()

  localStorage.setItem("token", json.token)

  return json
}

export type User = {
  username: string
  reputation: number
  pow: string
  md5: string
}

export type Program = {
  id: string
  name: string
  programType: number
  joined: boolean
}

export type Report = {
  title: string
  description: string
  severity: string
  published: number
  weakness: string
  programID: string
  programName: string
}

export async function getUser(): Promise<User> {
  const token = localStorage.getItem("token") ?? ""

  const response = await fetch(`/api/user/info`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 200) {
    throw new ApiError(response.status, "Unauthorized")
  }

  const json: User = await response.json()

  return json
}

export async function getDiscovery(): Promise<Report> {
  const token = localStorage.getItem("token") ?? ""
  const response = await fetch(`/api/discovery`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 200) {
    throw new ApiError(response.status, await response.text())
  }

  return await response.json()
}

export async function getPrograms(): Promise<Array<Program>> {
  const token = localStorage.getItem("token") ?? ""
  let response = await fetch(`/api/programs`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 200) {
    throw new ApiError(response.status, await response.text())
  }

  const programs: Array<Program> = await response.json()
  
  response = await fetch(`/api/program/joined`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 200) {
    throw new ApiError(response.status, await response.text())
  }

  const joinedPrograms: Array<string> = (await response.json()).programs

  for (const programID of joinedPrograms) {
    const p = programs.find((e) => e.id == programID)
    if (p !== undefined) {
      p.joined = true
    }
  }

  return programs
}

export async function createReport(description: string, title: string, severity: string, program: string): Promise<string> {
  const token = localStorage.getItem("token") ?? ""
  const weakness = "CWE-1"
  const response = await fetch(`/api/report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      description,
      title,
      severity,
      weakness,
      program
    }),
  })
  if (response.status !== 200) {
    throw new ApiError(response.status, await response.text())
  }

  return (await response.json())["reportID"]
}

export async function getReport(id: string, pow: string): Promise<Report> {
  const token = localStorage.getItem("token") ?? ""
  const response = await fetch(`/api/report/${id}?pow=${pow}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 200) {
    if (response.status === 404) {
      throw new ApiError(response.status, "Report not found")
    } else {
      throw new ApiError(response.status, await response.text())
    }
  }

  const report: Report = await response.json()

  return report
}

export async function importReputation(
  username: string,
  validator: string,
): Promise<void> {
  const token = localStorage.getItem("token") ?? ""
  const response = await fetch(`/api/user/import_reputation`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      username,
      validator,
    }),
  })

  if (response.status != 200) {
    const json: ErrorResponse = await response.json()
    throw new ApiError(response.status, json.message)
  }
}

export async function logout() {
  localStorage.removeItem("token")
}

export async function joinProgram(
  programID: string,
): Promise<void> {
  const token = localStorage.getItem("token") ?? ""
  const response = await fetch(`/api/program/${programID}/join`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status != 200) {
    const json: ErrorResponse = await response.json()
    throw new ApiError(response.status, json.message)
  }
}
