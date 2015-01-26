if(!window.OpinionStage) {
    window.OpinionStage = {};

    OpinionStage.state = {};
    OpinionStage.functions = {};
    OpinionStage.hooks = {};
    OpinionStage.polls = []; // Polls ids
    OpinionStage.sets = []; // Set ids
    OpinionStage.containers = []; // Containers ids
    OpinionStage.containers_data = {}; // Containers elements data including elements ids array and elements data
    OpinionStage.polls_locations = {};
    OpinionStage.sets_locations = {};
    OpinionStage.state.initialized = false;
    OpinionStage.state.ready = false;
    OpinionStage.protocol = document.location.protocol == "https:" ? "https:" : "http:";
    // JSON RegExp
    OpinionStage.rvalidchars = /^[\],:{}\s]*$/;
    OpinionStage.rvalidescape = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g;
    OpinionStage.rvalidtokens = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g;
    OpinionStage.rvalidbraces = /(?:^|:|,)(?:\s*\[)+/g;

    OpinionStage.functions.include = Array.prototype.indexOf ?
            function(arr, obj) { return arr.indexOf(obj) !== -1 && typeof arr.indexOf(obj) !== "undefined"; } :
            function(arr, obj) {
                for(var i = -1, j = arr.length; ++i < j;)
                    if(arr[i] === obj) return true;
                return false;
            };

    OpinionStage.trim = function (text) {
        if (text.trim) {
            return text == null ? "" : text.trim();
        }
        return text == null ? "" : text.toString().replace(/^\s+/,'').replace(/\s+$/,'');
    }
    // Code taken from jquery
    OpinionStage.parseJson = function(data) {
        try {
            if (typeof data !== "string" || !data) {
                return null;
            }
            data = OpinionStage.trim(data);
            if (window.JSON && window.JSON.parse) {
                return window.JSON.parse(data);
            }
            if (OpinionStage.rvalidchars.test(data.replace(OpinionStage.rvalidescape, "@")
                    .replace(OpinionStage.rvalidtokens, "]")
                    .replace(OpinionStage.rvalidbraces, ""))) {
                return ( new Function( "return " + data ) )();
            }
            return "";
        } catch(e) {
            return "";
        }
    }
    OpinionStage.addHook = function(side_id, code) {
        OpinionStage.hooks[side_id] = new Function(code);
    }
    OpinionStage.addNativeListener = function(event, callback) {
        return window.addEventListener ? window.addEventListener(event, callback, false) : window.attachEvent("on" + event, callback);
    }
    OpinionStage.handleMessage = function(evt) {
        // Verify the message came from 'opinionstage'
        if (evt.origin.indexOf("opinionstage.com") != -1) {
            var msg = OpinionStage.parseJson(evt.data);
            if ((msg.type == "heightChanged") && msg.data) {
                OpinionStage.setFrameHeight(OpinionStage.polls_locations[msg.data.poll_id], msg.data.height);
            } else if ((msg.type == "pollSetHeightChanged") && msg.data) {
                OpinionStage.setFrameHeight(OpinionStage.sets_locations[msg.data.set_id], msg.data.height);
            } else if ((msg.type == "redirect") && msg.data) {
                OpinionStage.redirect(msg.data.url);
            } else if ((msg.type == "pollVote") && msg.data) {
                if (OpinionStage.hooks[msg.data.sides[0]] != null) {
                    OpinionStage.hooks[msg.data.sides[0]]();
                }
            }
        }
    }
    OpinionStage.redirect = function(url) {
        window.location.href = url;
    }
    OpinionStage.shouldAddContainerElement = function(container_id, element_id) {
        // Match the url expression of the given container element against the current url parsed
        var regex = new RegExp("^" + OpinionStage.containers_data[container_id].elements[element_id].url_expression + "$", "i");
        // Remove the protocol and the www prefix
        var url = window.location.href.replace(/.*?:\/\//g, "").replace(/^www\./g, "");
        return regex.test(url);
    }
    OpinionStage.addContainerElement = function(container_id, element_id) {
        var container_element = OpinionStage.containers_data[container_id].elements[element_id];
        if (container_element.element_type == "Container::Element::Poll") {
            OpinionStage.addPollLocation(container_element.element_id, "container_" + container_id);
            OpinionStage.waitForCommunication(OpinionStage.embedPoll, {poll_id: container_element.element_id, width: container_element.width});
        } else if (container_element.element_type == "Container::Element::GroupSet") {
            OpinionStage.addPollSetLocation(container_element.element_id, "container_" + container_id);
            OpinionStage.waitForCommunication(OpinionStage.embedPollSet, {set_id: container_element.element_id, width: container_element.width});
        }
    }
    OpinionStage.assignContentToContainer = function(container_id) {
        for (i = 0; i < OpinionStage.containers_data[container_id].elements_ids.length; i++) {
            if (OpinionStage.shouldAddContainerElement(container_id, OpinionStage.containers_data[container_id].elements_ids[i])) {
                OpinionStage.addContainerElement(container_id, OpinionStage.containers_data[container_id].elements_ids[i]);
                break;
            }
        }
    }
    OpinionStage.initContainerLocations = function(container_id, container_elements_data) {
        if (OpinionStage.functions.include(OpinionStage.containers, container_id)) {
            return; // Container data was already initialized
        }
        OpinionStage.containers.push(container_id);
        OpinionStage.containers_data[container_id] = {elements_ids: [], elements: {}};

        for (i = 0; i < container_elements_data.length; i++) {
            var element_id = container_elements_data[i][0];
            OpinionStage.containers_data[container_id].elements[element_id] = {
                url_expression: container_elements_data[i][1],
                element_id: container_elements_data[i][2],
                element_type: container_elements_data[i][3],
                width: container_elements_data[i][4]};
            OpinionStage.containers_data[container_id].elements_ids.push(element_id);
        }
    }
    OpinionStage.addPollLocation = function(poll_id, div_id) {
        OpinionStage.polls_locations[poll_id] = div_id;
    }
    OpinionStage.insertLoader = function(div_id) {
        var container_div = document.getElementById(div_id);
        var existing_loader = OpinionStage.getElementsByClassName(container_div, "os-loader")[0];
        if (existing_loader != null) {
            return; // Not adding a second loader
        }
        var loader = document.createElement('div');
        loader.className = "os-loader";
        loader.setAttribute('style','background: url(https://d15r06k2ko210l.cloudfront.net/assets/ajax-loader-107b480a27602c4d837308f058a18df5.gif) no-repeat;height: 32px; width: 32px; display: block; margin: 0 auto !important');
        container_div.insertBefore(loader, container_div.firstChild);
    }
    OpinionStage.addPollSetLocation = function(set_id, div_id) {
        OpinionStage.sets_locations[set_id] = div_id;
    }
    OpinionStage.setFrameHeight = function(frame_container_id, height) {
        var frame_div = document.getElementById(frame_container_id);
        if (frame_div != null) {
            var frame = frame_div.getElementsByTagName("IFRAME")[0];
            var current_style = frame.style.cssText;
            if (current_style.indexOf('height') == -1) {
                OpinionStage.hideLoader(frame_container_id);
            }
            frame.style.cssText = "height: " + height + "px !important";
        }
    }
    OpinionStage.embedPoll = function(args) {
        if (!OpinionStage.functions.include(OpinionStage.polls, args.poll_id)) {
            OpinionStage.polls.push(args.poll_id);
            OpinionStage.insertIframe("/polls/" + args.poll_id + "/poll", args.width, OpinionStage.polls_locations[args.poll_id])
        }
    }
    OpinionStage.embedPollSet = function(args) {
        if (!OpinionStage.functions.include(OpinionStage.sets, args.set_id)) {
            OpinionStage.sets.push(args.set_id);
            OpinionStage.insertIframe("/sets/" + args.set_id + "/iframe", args.width, OpinionStage.sets_locations[args.set_id])
        }
    }
    OpinionStage.insertIframe = function(path, width, div_id) {
        // Add the iframe with height 0 until visible
        var frame = document.createElement('iframe');
        frame.setAttribute('width', width);
        frame.setAttribute('height','0');
        frame.setAttribute('frameBorder','0');
        frame.setAttribute('scrolling','no');
        frame.setAttribute('style','border: none;margin-bottom: 0 !important');
        frame.setAttribute("src", OpinionStage.protocol + "//www.opinionstage.com" + path);
        frame.setAttribute('name', 'os_frame');
        var frame_div = document.getElementById(div_id);
        frame_div.insertBefore(frame, frame_div.firstChild);
    }

    OpinionStage.getElementsByClassName= function(node, classname) {
        // getElementsByClassName not supported in IE8
        if (typeof node.getElementsByClassName !== "undefined") {
            return node.getElementsByClassName(classname);
        }
        var a = [];
        var re = new RegExp('(^| )' + classname + '( |$)');
        var els = node.getElementsByTagName("*");
        for(var i=0,j=els.length; i<j; i++)
            if(re.test(els[i].className))a.push(els[i]);
        return a;
    }

    OpinionStage.hideLoader = function(div_id) {
        var container_div = document.getElementById(div_id);
        if (container_div != null) {
            var loader = OpinionStage.getElementsByClassName(container_div, "os-loader")[0];
            if (loader != null) {
                loader.style.cssText = "display: none";
            }
        }
    }

    OpinionStage.waitForCommunication = function(callback, args) {
        if (OpinionStage.state.ready == false) {
            setTimeout(function() { OpinionStage.waitForCommunication(callback, args) } , 100);
        } else {
            callback(args);
        }
    }
    OpinionStage.firstTimeInit = function() {
        if (!OpinionStage.state.initialized) {
            OpinionStage.state.initialized = true;
            // Register to the post message method
            OpinionStage.addNativeListener("message", OpinionStage.handleMessage);
            OpinionStage.state.ready = true;
        }
    }
    OpinionStage.firstTimeInit();
}
OpinionStage.addPollLocation(2229111, "debate_1_" + 2229111);
OpinionStage.insertLoader("debate_1_" + 2229111);
OpinionStage.waitForCommunication(OpinionStage.embedPoll, {poll_id: 2229111, width: '100%'});