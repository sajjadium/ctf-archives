'use client'
import Image from 'next/image'
import styles from './page.module.css'
import { useState } from 'react';
import Link from 'next/link';



export default function Home() {
  return (

    <main className={styles.main}>
    <h1>InsoBank</h1>
      <div className={styles.description}>
        <p>At InsoBank, we're transforming the way you bank with a commitment to innovation and excellence. Bid farewell to traditional banking woes and embrace a secure, intuitive, and forward-thinking financial experience with us. Discover why InsoBank is your premier destination for next-generation online banking</p>
      </div>
      <div className={styles.grid}>
      <span>
        <h3>
          Innovative Savings Solutions
        </h3>
        <p>
          Optimize your savings with our innovative tools. From automated round-ups to goal-oriented savings plans, InsoBank provides creative solutions to accelerate your progress toward financial objectives.
        </p>
        </span>
        <span>
          <h3>
            Transparent Pricing
          </h3>
          <p>Say goodbye to hidden fees. InsoBank is dedicated to transparency, offering a banking experience that is clear of concealed charges. We believe in providing fair and straightforward financial services.</p>
        </span>

        <span>
          <h3>
            Intelligent Banking, Empowering You
          </h3>
          <p>
            Engage with banking that evolves with you. Our state-of-the-art technology adapts to your financial habits, delivering personalized insights and recommendations to empower you in making informed decisions.
          </p>
        </span>
                <span>
          <h3>
            Seamless User Experience
          </h3>
          <p>
            Enjoy a smooth and visually appealing interface designed for ease of use. Whether you're managing accounts, conducting transactions, or exploring advanced financial tools, it's all conveniently accessible at your fingertips.
          </p>
        </span>
                <span>
          <h3>
            Fortified Security
          </h3>
          <p>
            Rest easy knowing your security is our top priority. InsoBank employs cutting-edge measures, such as advanced encryption and biometric authentication, to safeguard your financial data against any potential threats.
          </p>
        </span>
                <span>
          <h3>
            Instant Transactions, Anytime, Anywhere
          </h3>
          <p>
            Experience the speed of instant transactions and real-time updates. Whether you're transferring funds, settling bills, or overseeing investments, everything occurs in the blink of an eye, giving you more control over your time.
          </p>
        </span>
      </div>
      <div className={styles.description}>
        <p>Join InsoBank today and step into a new era of banking. Elevate your financial journey with technology that understands you and services that surpass your expectations. Welcome to banking reimagined – Welcome to InsoBank!</p>
      </div>
    </main>
  )
}
