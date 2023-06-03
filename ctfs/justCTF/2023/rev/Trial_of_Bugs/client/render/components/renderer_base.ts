import {Component} from "../../../share/entity/component";
import {GameMapRenderer} from "../game_map_renderer";

export class RendererBase extends Component {
    get renderer(): GameMapRenderer {
        return this.entity.world.getSingleton(GameMapRenderer);
    }

    get gl(): WebGLRenderingContext {
        return this.renderer.gl;
    }

    render() {
    }

    get renderLayer() {
        return 1;
    }
}
