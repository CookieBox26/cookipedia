(function () {
  if (typeof Prism === 'undefined' || typeof document === 'undefined') {
    return;
  }
  Prism.hooks.add(
    'before-sanity-check',
    function (env) {
      env.code = env.code.replace(/^(?:\r?\n|\r)/, '');
    }
  );
})();
