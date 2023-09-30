import {
  FingerPrintIcon,
  HeartIcon,
  LockClosedIcon,
} from "@heroicons/react/24/outline";
import React from "react";

function HomePage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center px-2 text-white">
      <h1 className="mb-20 text-5xl font-bold">Ogrechat</h1>

      <div className="flex space-x-2 text-center">
        <div>
          <div className="mb-5 flex flex-col items-center justify-center">
            <FingerPrintIcon className="h-6 w-6" />
            <h2>Private</h2>
          </div>

          <div className="space-y-2">
            <p className="infoText">
              Military grade encryption empowers your communications to be safe
              from prying eyes
            </p>
            <p className="infoText">
              Just like how ogres are like onions because they have layers, this
              site is like an onion because it&apos;s exclusively hosted on the
              Onion network
            </p>
            <p className="infoText">
              No sign-up required, just jump straight into chatting
            </p>
          </div>
        </div>

        <div>
          <div className="mb-5 flex flex-col items-center justify-center">
            <LockClosedIcon className="h-6 w-6" />
            <h2>Secure</h2>
          </div>

          <div className="space-y-2">
            <p className="infoText">
              With our zero JavaScript frontend requirements, you can rest
              assured there&apos;s no fishy tracking
            </p>
            <p className="infoText">
              Our open-source first approach to development lets you keep us
              honest
            </p>
            <p className="infoText">
              Rigorously and frequently audited to ensure our ambitious feature
              updates don&apos;t compromise on security and help keep the site
              up and running
            </p>
          </div>
        </div>

        <div>
          <div className="mb-5 flex flex-col items-center justify-center">
            <HeartIcon className="h-6 w-6" />
            <h2>Supported by you</h2>
          </div>

          <div className="space-y-2">
            <p className="infoText">
              Spread the word on how our services helped you in your endeavours
            </p>
            <p className="infoText">
              Donate XMR to help financially fund development
            </p>
            <p className="infoText">
              Join the our forum and interact with the growing community
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
