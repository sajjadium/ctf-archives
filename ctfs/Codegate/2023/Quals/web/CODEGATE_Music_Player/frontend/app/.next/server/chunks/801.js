"use strict";
exports.id = 801;
exports.ids = [801];
exports.modules = {

/***/ 1801:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "n": () => (/* binding */ AudioProvider),
/* harmony export */   "x": () => (/* binding */ useAudioPlayer)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5893);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6689);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const AudioPlayerContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)();
const reducers = {
    SET_META (state, action) {
        return {
            ...state,
            meta: action.payload
        };
    },
    PLAY (state, _action) {
        return {
            ...state,
            playing: true
        };
    },
    PAUSE (state, _action) {
        return {
            ...state,
            playing: false
        };
    },
    TOGGLE_MUTE (state, _action) {
        return {
            ...state,
            muted: !state.muted
        };
    },
    SET_CURRENT_TIME (state, action) {
        return {
            ...state,
            currentTime: action.payload
        };
    },
    SET_DURATION (state, action) {
        return {
            ...state,
            duration: action.payload
        };
    }
};
function audioReducer(state, action) {
    return reducers[action.type](state, action);
}
function AudioProvider({ children  }) {
    let [state, dispatch] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useReducer)(audioReducer, {
        playing: false,
        muted: false,
        duration: 0,
        currentTime: 0,
        meta: null
    });
    let playerRef = (0,react__WEBPACK_IMPORTED_MODULE_1__.useRef)(null);
    let actions = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(()=>{
        return {
            play (data) {
                if (data) {
                    dispatch({
                        type: "SET_META",
                        payload: data
                    });
                    if (playerRef.current.currentSrc !== data.audio.src) {
                        let playbackRate = playerRef.current.playbackRate;
                        playerRef.current.src = data.audio.src;
                        playerRef.current.load();
                        playerRef.current.pause();
                        playerRef.current.playbackRate = playbackRate;
                        playerRef.currentTime = 0;
                    }
                }
                playerRef.current.play();
            },
            pause () {
                playerRef.current.pause();
            },
            toggle (data) {
                this.isPlaying(data) ? actions.pause() : actions.play(data);
            },
            seekBy (amount) {
                playerRef.current.currentTime += amount;
            },
            seek (time) {
                playerRef.current.currentTime = time;
            },
            playbackRate (rate) {
                playerRef.current.playbackRate = rate;
            },
            toggleMute () {
                dispatch({
                    type: "TOGGLE_MUTE"
                });
            },
            isPlaying (data) {
                return data ? state.playing && playerRef.current.currentSrc === data.audio.src : state.playing;
            }
        };
    }, [
        state.playing
    ]);
    let api = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(()=>({
            ...state,
            ...actions
        }), [
        state,
        actions
    ]);
    return /*#__PURE__*/ (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {
        children: [
            /*#__PURE__*/ react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx(AudioPlayerContext.Provider, {
                value: api,
                children: children
            }),
            /*#__PURE__*/ react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx("audio", {
                ref: playerRef,
                onPlay: ()=>dispatch({
                        type: "PLAY"
                    }),
                onPause: ()=>dispatch({
                        type: "PAUSE"
                    }),
                onTimeUpdate: (event)=>{
                    dispatch({
                        type: "SET_CURRENT_TIME",
                        payload: Math.floor(event.target.currentTime)
                    });
                },
                onDurationChange: (event)=>{
                    dispatch({
                        type: "SET_DURATION",
                        payload: Math.floor(event.target.duration)
                    });
                },
                muted: state.muted
            })
        ]
    });
}
function useAudioPlayer(data) {
    let player = (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(AudioPlayerContext);
    return (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(()=>({
            ...player,
            play () {
                player.play(data);
            },
            toggle () {
                player.toggle(data);
            },
            get playing () {
                return player.isPlaying(data);
            }
        }), [
        player,
        data
    ]);
}


/***/ })

};
;