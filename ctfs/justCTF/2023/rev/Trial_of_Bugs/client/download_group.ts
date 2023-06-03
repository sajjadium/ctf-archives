import {ObservableField} from "../share/util/observable_field";

export type DownloadGroupStatus = {
    allRequests: number,
    completeRequests: number
}

export class DownloadGroup {
    state= new ObservableField<DownloadGroupStatus>({allRequests: 0, completeRequests: -1});
    private completeCb: () => void = () => {};
    private finalized: boolean = false;

    constructor(cb: () => void) {
        this.completeCb = cb;
    }

    loadJsonAsset(path: string, cb: (data: any) => void) {
        this._onRequestStart();
        fetch(path).then((rsp: any) => rsp.json()).then((data: any) => {
            cb(data);
            this._onRequestComplete();
        });
    }

    loadImageAsset(path: string, cb: (image: HTMLImageElement) => void) {
        this._onRequestStart();
        const img = new Image();
        img.onload = () => {
            cb(img);
            this._onRequestComplete();
        };
        img.src = path;
    }

    loadJsAsset(path: string, cb: () => void) {
        this._onRequestStart();
        const script = document.createElement('script');
        script.onload = () => {
            cb();
            document.head.removeChild(script);
            this._onRequestComplete();
        };
        script.src = path;
        document.head.appendChild(script);
    }

    finalize() {
        this.finalized = true;
        this._onRequestComplete();
    }

    protected _onRequestStart() {
        if (this.finalized)
            throw new Error('Download group already finalized!');

        const prevState = this.state.get();
        this.state.set({ ...prevState, allRequests: prevState.allRequests + 1 });
    }

    protected _onRequestComplete() {
        const prevState = this.state.get();
        this.state.set({ ...prevState, completeRequests: prevState.completeRequests + 1 });
        if (prevState.completeRequests + 1 === prevState.allRequests)
            this.completeCb();
    }
}
