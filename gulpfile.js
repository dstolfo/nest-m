var gulp = require('gulp'),
    merge = require('merge-stream'),
    runSequence = require('run-sequence'),
    browserify = require('browserify'),
    transform = require('vinyl-transform'),
    _ = require('underscore'),
    fs = require('fs'),
    ini = require('ini'),
    del = require('del');

// read local configuration file
var local_ini = './config/config.ini';
config = ini.parse(fs.readFileSync(local_ini, 'utf-8'));

// copy static files from analytics-web applications to public_dist
gulp.task('copy_static', function() {
    return gulp.src(["./web/nest_m/static/**/*"])
        .pipe(gulp.dest(config.build.public_dir));
});

// build js modules for front end
gulp.task('browserify', ['copy_static'], function() {
    var browserified = transform(function(filename) {
        var b = browserify(filename);
        return b.bundle()
    });
    var src_dir = config.build.public_dir + '/js/';
    return gulp.src([src_dir + '/**/*.js'])
        .pipe(browserified)
        .pipe(gulp.dest(src_dir));
});

// bundle bootstrap resources for browser
gulp.task('bootstrap', function() {
    return gulp.src([config.build.node_dir + '/bootstrap/dist/**/*'])
        .pipe(gulp.dest(config.build.public_dir + '/bootstrap'));
});

// bundle reveal.js resources for browser
gulp.task('reveal.js', function() {
    var lib = gulp.src([config.build.node_dir + '/reveal.js/lib/**/*'])
        .pipe(gulp.dest(config.build.public_dir + '/lib'));
    var css = gulp.src([config.build.node_dir + '/reveal.js/css/**/*'])
        .pipe(gulp.dest(config.build.public_dir + '/reveal'));
    return merge(lib, css);
});

// clean ./public_dist
gulp.task('clean', function(cb) {
    del([config.build.public_dir], cb);
});

gulp.task('build', function(cb) {
    runSequence('clean', ['browserify', 'bootstrap', 'reveal.js'], cb);
});

gulp.task('default', ['build']);
