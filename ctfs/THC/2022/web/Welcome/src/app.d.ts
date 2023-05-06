/* eslint-disable @typescript-eslint/no-unused-vars */
/// <reference types="@sveltejs/kit" />

import type { User } from '@prisma/client'

// See https://kit.svelte.dev/docs/typescript
// for information about these interfaces
global {
  import type { Socket } from 'socket.io-client'
  interface Window {
    socketClient: Socket | undefined
  }

  declare namespace App {
    interface Locals {
      mobile: boolean
      user: User | null
    }

    // eslint-disable-next-line @typescript-eslint/no-empty-interface
    interface Platform {}

    interface Session {
      mobile: boolean
      user: User | null
    }

    interface Stuff {
      title: string
    }
  }

  interface ImportMetaEnv {
    VITE_API_PORT: string
    VITE_TENOR_KEY: string
  }
}
