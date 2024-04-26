'use client'

import { Inter } from 'next/font/google'
import Link from 'next/link';
import './globals.css'
import styles from './page.module.css'
import { useContext, useState } from 'react';
import { AppWrapper, useAppContext } from './appContext.js';

const inter = Inter({ subsets: ['latin'] })

function Menu() {
  
  const { userid, setUserid, API_ROOT } = useAppContext();

  return(
    <div className={styles.menu}>
      <Link href="/">
        <div className={styles.menuitem}>
          Home
        </div>
      </Link>
      <Link href="/account">
        <div className={styles.menuitem}>
          Accounts
        </div>
      </Link>
      <Link href="/transactions">
        <div className={styles.menuitem}>
          Transactions
        </div>
      </Link>
      <Link href="/profile">
        <div className={styles.menuitem}>
          Profile
        </div>
      </Link>
      {!userid && 
        <Link href="/auth/login">
          <div className={styles.menuitem}>
            Login
          </div>
        </Link>
      }
      {!userid && 
        <Link href="/auth/register">
          <div className={styles.menuitem}>
            Register
          </div>
        </Link>
      }
      {userid && 
        <Link href="/auth/logout">
          <div className={styles.menuitem}>
            Logout
          </div>
        </Link>
      }

    </div>
  )
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {

  return (
    <html lang="en">
      <AppWrapper>
      <body className={inter.className}>
      <div className={styles.main}>
        <Menu/>
        {children}
      </div>
      </body>
      </AppWrapper>
    </html>
  )
}
