import * as React from "react";
import { Button, Code, Frame, Input } from "react-pwn";
import { toast } from "react-toastify";

import { api } from "../../client";
import { SiteContext, SiteProvider } from "../../providers/site-provider";

import "./index.scss";

export interface Props {};

const _SiteList = (props: Props) => {
    const { sites, refresh } = React.useContext(SiteContext);

    const lock = React.useRef(false);
    const [domainName, setDomainName] = React.useState("");

    if (sites.loading && !sites.value) {
        return (
            <>Loading...</>
        );
    }

    if (!sites.value) {
        return <>Something went wrong</>;
    }

    const validateSite = async (domain: string) => {
        if (lock.current) return;
        lock.current = true;
        try {
            await api.site.validate(domain);
            toast.success(`${domain} verified!`);
        } catch (e) {
            toast.error(e);
        }
        await refresh();
        lock.current = false;
    };
    const scrapeSite = async (domain: string) => {
        if (lock.current) return;
        lock.current = true;
        try {
            await api.site.scrape(domain);
            toast.success(`${domain} scraped!`);
        } catch (e) {
            toast.error(e);
        }
        await refresh();
        lock.current = false;
    };
    const registerDomain = async () => {
        if (lock.current) return;
        lock.current = true;
        try {
            await api.site.register(domainName);
            toast.success(`${domainName} registered!`);
        } catch (e) {
            toast.error(e);
        }
        await refresh();
        lock.current = false;
    }

    const orderedSites = sites.value.sort((s1, s2) => s1.pending === s2.pending ? s1.domain.localeCompare(s2.domain) : s1.pending ? 1 : -1);

    return (
        <>
            <Frame className="domain-registration">
                <div className="title">Register Domain</div>
                <Input value={domainName} onChange={setDomainName} placeholder={"Domain Name"} onEnter={registerDomain}/>
                <Button label={"Register"} onClick={registerDomain}/>
            </Frame>
            <Frame>
                <div className="title">Registered Domains</div>
                {
                    orderedSites.map((site) => (
                        site.pending
                            ? (
                                <div className="site pending-site" key={site.domain}>
                                    <div className="site-domain">{ site.domain }</div>
                                    <div className="site-content">
                                        <div className="site-validation">
                                            To validate this site, add a new <Code inline>TXT</Code> record with the value <Code inline>wowza-domain-verification={ site.validationCode }</Code>.
                                        </div>
                                        <Button label="Validate Now" onClick={() => validateSite(site.domain)}/>
                                    </div>
                                </div>
                            )
                            : (
                                <div className="site" key={site.domain}>
                                    <div className="site-domain">{ site.domain }</div>
                                    <div className="site-content">
                                        <Button label="Scrape Now" onClick={() => scrapeSite(site.domain)}/>
                                    </div>
                                </div>
                            )
                    ))
                }
            </Frame>
        </>
    )
};

export const SiteList = (props: Props) => (
    <SiteProvider>
        <_SiteList {...props}/>
    </SiteProvider>
);