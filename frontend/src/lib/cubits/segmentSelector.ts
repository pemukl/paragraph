
import type { TextSegment } from "$lib/segment";
import { subscribe } from "svelte/internal";
import { writable } from "svelte/store";

class SegmentSelector {
    _subscribe: any;
    _set: (this: void, value: TextSegment) => void;
    _update: any;

    _previous: TextSegment;

    constructor(initialSegment: TextSegment) {
        const { subscribe, set, update } = writable<TextSegment>(initialSegment);
        this._subscribe = subscribe;
        this._set = set;
        this._update = update;
        this._previous = initialSegment;
    }

    get store() {
        return {
            subscribe,
            select: (segment: TextSegment) => this._update(segment),
            reset: () => this._set(this._previous),
        }
    };


}