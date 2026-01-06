window.dash_clientside = Object.assign({}, window.dash_clientside, {
    animation: {
        step_forward: function(n_intervals, step, store) {
            if (!store || !store.history) {
                return step || 0;
            }

            const maxStep = store.history.length - 1;

            if (step === null || step === undefined) {
                return 0;
            }

            return Math.min(step + 1, maxStep);
        }
    }
});
