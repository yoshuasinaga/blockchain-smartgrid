# CountUp.js
CountUp.js is a dependency-free, lightweight JavaScript "class" that can be used to quickly create animations that display numerical data in a more interesting way.

Despite its name, CountUp can count in either direction, depending on the `startVal` and `endVal` params that you pass.

CountUp.js supports all browsers.

## [Try the demo](http://inorganik.github.io/countUp.js)

## See Also

- **[CountUp.js Angular ^2 Module](https://github.com/inorganik/countUp.js-angular2)** ![New and improved!](http://img4me.com/sxa.gif)
- **[CountUp.js Angular 1.x Module](https://github.com/inorganik/countUp.js-angular1)**
- **[CountUp.js React](https://github.com/glennreyes/react-countup)**
- **[CountUp.js Vue component wrapper](https://github.com/xlsdg/vue-countup-v2)**
- **[CountUp.js WordPress Plugin](https://wordpress.org/plugins/countup-js/)**

## Installation

Simply include the countUp.js file in your project or install via npm/yarn using the package name `countup.js`.

Before making a pull request, please [read this](#contributing). MIT License.

A jQuery version is also included, but needs to be included manually.

## Usage:
Params:
- `target` = id of html element, input, svg text element, or var of previously selected element/input where counting occurs
- `startVal` = the value you want to begin at
- `endVal` = the value you want to arrive at
- `decimals` = (optional) number of decimal places in number, default 0
- `duration` = (optional) duration in seconds, default 2
- `options` = (optional, see demo) formatting/easing options object

Decimals, duration, and options can be left out to use the default values.

```js
var numAnim = new CountUp("SomeElementYouWantToAnimate", 24.02, 99.99);
if (!numAnim.error) {
    numAnim.start();
} else {
    console.error(numAnim.error);
}
```

with optional callback:

```js
numAnim.start(someMethodToCallOnComplete);

// or an anonymous function
numAnim.start(function() {
    // do something
})
```

#### Other methods:
Toggle pause/resume:

```js
numAnim.pauseResume();
```

Reset an animation:

```js
numAnim.reset();
```

Update the end value and animate:

```js
var someValue = 1337;
numAnim.update(someValue);
```

#### Animating to large numbers
For large numbers, since CountUp has a long way to go in just a few seconds, the animation seems to abruptly stop. The solution is to subtract 100 from your `endVal`, then use the callback to invoke the `update` method which completes the animation with the same duration with a difference of only 100 to animate:
```js
var endVal = 9645.72;
var numAnim = new CountUp('targetElem', 0, endVal - 100, 2, duration/2);
numAnim.start(function() {
	numAnim.update(endVal);
});
```

## Contributing <a name="contributing"></a>

Before you make a pull request, please be sure to follow these instructions:

1. Do your work on `countUp.js` and/or other files in the root directory.
2. In Terminal, `cd` to the `countUp.js` directory.
3. Run `npm i`
4. Run `npm run build`, which copies and minifies the .js files to the `dist` folder.
