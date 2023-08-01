/** @odoo-module **/
const { whenReady, Component } = owl;
import { setupAndMount } from '@website_octoopus/js/owl'
import { DynamicPlaceholderInput } from '@website_octoopus/js/dynamic_placeholder_input/component';

whenReady(() => setupAndMount(MainSearchBar));


export class DynamicSearchBar extends DynamicPlaceholderInput {
    _id = "dsb";

    async getPlaceholderValues(){
        // Todo someday: generate phrases randomly
        return [
            "A medieval piece played on a hurdy-gurdy and accompanied by a singing frog",
            "An orchestral piece inspired by the sound of raindrops and thunderstorms",
            "A piece composed for a glass harmonica and a theremin that creates a mysterious atmosphere",
            "I want to hear a duet between a tuba and a kazoo that makes me laugh",
            "A Baroque fugue played on a pipe organ with at least 4 voices",
            "A music piece where the only percussion instruments are kitchen utensils",
            "The most energetic and danceable piece composed for an accordion and a balalaika",
            "A symphony composed for a full orchestra where each instrument mimics the sound of different animals",
            "An experimental piece played on instruments made of ice that slowly melts during the performance",
            "A jazz improvisation featuring a didgeridoo, a sitar, and a banjo",
            "A contemporary piece for an ensemble of human beatboxers and vocalists, replicating the sounds of a string quartet",
            "A musical battle between a piano and a set of bongo drums, where each instrument tries to outshine the other",
            "A romantic ballad played by a ukulele and a cello with lyrics inspired by the beauty of nature",
            "An epic rock opera performed by a mariachi band with a guest appearance of a virtuoso accordion player",
            "A soothing lullaby featuring a harp and a choir of humming voices",
            "A piece where the only instruments are whistling and finger snapping, creating a surprisingly complex melody and rhythm",
            "An electronic dance track featuring traditional Chinese instruments like the erhu, guzheng, and pipa",
            "A relaxing piano piece inspired by the sound of waves crashing on the shore",
            "A lively jazz trio featuring a trumpet, double bass, and drums",
            "A classical guitar piece that evokes the atmosphere of a Spanish village",
            "A flute concerto composed in the 18th century with a lively third movement",
            "A baroque piece for harpsichord inspired by the theme of birdsong",
            "A string quartet that captures the essence of a peaceful walk through a forest",
            "A 20th-century orchestral piece that incorporates elements of folk music from Eastern Europe",
            "A bossa nova song with smooth vocals and gentle guitar accompaniment",
            "A modern reinterpretation of a famous opera aria, arranged for a chamber ensemble",
            "A catchy pop song that features a prominent saxophone solo",
            "A beautiful nocturne for piano composed during the Romantic era",
            "An energetic bluegrass tune featuring banjo, fiddle, and mandolin",
            "A soulful ballad with a powerful vocal performance and a rich orchestral background",
            "A serene choral piece with lyrics inspired by the poetry of William Blake",
            "A brass quintet that showcases the virtuosity of each instrument",
            "A tango infused with the passion and rhythm of Argentine music",
            "A captivating movie soundtrack that transports the listener to a world of adventure",
            "A delightful waltz composed for a full symphony orchestra",
            "A minimalist piece for solo cello that explores the depths of the instrument's range",
            "An upbeat swing tune featuring a lively clarinet and saxophone",
            "A hauntingly beautiful composition for violin and piano",
            "A joyful march performed by a military brass band",
            "A Latin jazz fusion piece with a pulsating rhythm and catchy melodies",
            "A baroque suite for solo harp that showcases the beauty and complexity of the instrument",
            "An intimate vocal duet with delicate piano accompaniment",
            "An evocative piece for solo flute inspired by the beauty of the countryside",
            "A contemporary classical work that blends orchestral and electronic elements",
            "A rousing orchestral overture that captures the excitement of a grand celebration",
            "A spirited polka that invites listeners to dance and enjoy the lively tempo",
            "A serene and meditative piece for solo piano inspired by the tranquility of nature",
        ].sort(() => {
            return Math.random() - 0.5;
        });

    }
}



export class MainSearchBar extends Component {}
MainSearchBar.components = { DynamicSearchBar };
MainSearchBar.template = 'website_octoopus.MainSearchBar';