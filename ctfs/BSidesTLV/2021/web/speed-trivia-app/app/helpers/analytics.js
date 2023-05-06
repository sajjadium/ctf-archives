const ANALYTICS_LIMIT = process.env.ANALYTICS_LIMIT || 150;

async function waitfor(ms) {
    return await new Promise((resolve, reject) => {
        setTimeout(function(){ resolve(1); }, ms);
    }); 
}

async function analyticsSdk(event_to_report) {
    /*
        this method sends a request to the analytics microservice (http://one-of-our-internal/report)
    */
}

async function reportAnalytics(analytics) {
    let analyticsObj = {};
    let curr_event = '';

    if(analytics.length <= ANALYTICS_LIMIT) {   // Anti-DoS protection
        for(i = 0; i < analytics.length; i++) {
            if(analytics[i].toString().startsWith('event_')) {
                curr_event = analytics[i];
                analyticsObj[`event_${i}`] = curr_event;
                analyticsSdk(curr_event);   // TODO: tell devops to make this microservice RESPOND FASTER!
                await waitfor(10);          // Keep this dirty hack until devops answers back
            }
        }
    }
    console.log(`ANALYTICS SENT :: ` , analyticsObj); // log out a copy of everything we sent to the microservice
    return analyticsObj;
}

module.exports = { reportAnalytics }